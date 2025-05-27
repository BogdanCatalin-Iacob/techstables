from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Post model, handling serialization and validation
    of post data. It includes fields for owner details, timestamps, and
    content, and provides methods to verify if the current user is the
    post owner and to retrieve the like ID for the post. The serializer
    also validates the image size and dimensions.

    Attributes:
        owner (ReadOnlyField): The username of the post owner.
        profile_id (ReadOnlyField): The ID of the owner's profile.
        profile_image (ReadOnlyField): The URL of the owner's profile image.
        is_owner (SerializerMethodField): Indicates if the current user
            is the owner of the post.
        like_id (SerializerMethodField): The ID of the like by the current
            user on the post, if it exists.

    Methods:
        validate_image(value): Validates the size and dimensions of the image.
        get_is_owner(obj): Determines if the current user is the owner of the post.
        get_like_id(obj): Retrieves the like ID for the post by the current user.

    Meta:
        model (Model): The Post model.
        fields (list): List of fields to be serialized.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()

    def validate_image(self, value):
        '''
        Validates the uploaded image to ensure it meets size and dimension constraints.

        Args:
            value: The image file to be validated.

        Raises:
            serializers.ValidationError: If the image exceeds the maximum allowed size
            of 2MB, or if its height or width exceeds 4096 pixels.
        '''
        if not value:
            return
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image larger than 2MB!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height is larger than 4096 pixels'
            )
        if value.image.width > 4096:
            serializers.ValidationError(
                'Image width is larger than 4096 pixels'
            )

    def get_is_owner(self, obj):
        '''
        Determines if the requesting user is the owner of the post instance
        being serialized.

        Parameters:
            obj: The post instance being serialized.

        Returns:
            bool: True if the requesting user is the owner of the post,
            otherwise False.
        '''
        request = self.context['request']
        return obj.owner == request.user

    def get_like_id(self, obj):
        '''
        Retrieves the ID of the 'Like' instance associated
        with the current user and the specified post object.

        Args:
            obj: The post object for which the like ID is being retrieved.

        Returns:
            int or None: The ID of the 'Like' instance
                if it exists and the user is authenticated;
                otherwise, None.
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        '''
        Metadata options for the Post serializer.

        Attributes:
            model (Model): Specifies the model that the serializer is associated with, in this case, the Post model.
            fields (list): A list of fields that should be included in the serialized output. This includes:
                - 'id': The unique identifier for the post.
                - 'owner': The user who created the post.
                - 'is_owner': A boolean indicating if the current user is the owner of the post.
                - 'profile_id': The ID of the owner's profile.
                - 'profile_image': The URL of the owner's profile image.
                - 'created_at': The timestamp when the post was created.
                - 'updated_at': The timestamp when the post was last updated.
                - 'title': The title of the post.
                - 'content': The content of the post.
                - 'image': The image associated with the post.
                - 'like_id': The ID of the like by the current user on the post, if it exists.
        '''
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image',
            'like_id'
        ]
