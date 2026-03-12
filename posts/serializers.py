from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Post model, including additional fields for user-related
    information and post statistics.

    Attributes:
        owner (ReadOnlyField): The username of the post owner.
        profile_id (ReadOnlyField): The ID of the owner's profile.
        profile_image (ReadOnlyField): The URL of the owner's profile image.
        is_owner (SerializerMethodField): Indicates if the requesting user
            is the post owner.
        like_id (SerializerMethodField): The ID of the like by the current
            user on the post.
        comments_count (ReadOnlyField): The number of comments on the post.
        likes_count (ReadOnlyField): The number of likes on the post.

    Methods:
        validate_image: Validates the image size and dimensions.
        get_is_owner: Checks if the requesting user is the owner of the post.
        get_like_id: Retrieves the like ID for the current user and post.

    Meta:
        model: The Post model.
        fields: The fields to be serialized.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        '''
        Validates the uploaded image to ensure it meets size and
        dimension constraints.

        Args:
            value: The image file to be validated.

        Raises:
            serializers.ValidationError: If the image exceeds
            the maximum allowed size of 2MB,
            or if its height or width exceeds 4096 pixels.
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
            raise serializers.ValidationError(
                'Image width is larger than 4096 pixels'
            )
        return value

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
        Meta class for the Post serializer, defining the model
        and fields to be serialized.

        Attributes:
            model (Model): The model class that the serializer is based on,
                in this case, the Post model.
            fields (list): A list of field names to be included
                in the serialized output. This includes:
                - 'id': The unique identifier for the post.
                - 'owner': The username of the post owner.
                - 'is_owner': A boolean indicating if the current user
                    is the owner of the post.
                - 'profile_id': The ID of the owner's profile.
                - 'profile_image': The URL of the owner's profile image.
                - 'created_at': The timestamp when the post was created.
                - 'updated_at': The timestamp when the post was last updated.
                - 'title': The title of the post.
                - 'content': The content of the post.
                - 'image': The image associated with the post.
                - 'like_id': The ID of the like by the current user
                    on the post.
                - 'comments_count': The number of comments on the post.
                - 'likes_count': The number of likes on the post.
        '''
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image',
            'like_id', 'comments_count', 'likes_count'
        ]
