from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Comment model, providing fields for comment details
    and additional user-related information.

    Attributes:
        owner (ReadOnlyField): The username of the comment owner.
        is_owner (SerializerMethodField):
            Indicates if the request user is the owner.
        profile_id (ReadOnlyField): The ID of the owner's profile.
        profile_image (ReadOnlyField): The URL of the owner's profile image.
        created_at (SerializerMethodField): Human-readable creation time.
        updated_at (SerializerMethodField): Human-readable last update time.

    Methods:
        get_is_owner(obj): Determines if the request user
            is the owner of the comment.
        get_created_at(obj): Returns a human-readable creation time.
        get_updated_at(obj): Returns a human-readable last update time.

    Meta:
        model (Comment): The model that is being serialized.
        fields (list): The fields to be included in the serialized output.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        '''
        Determines if the current request user is
            the owner of the given object.

        Args:
            obj: The object instance being serialized.

        Returns:
            bool: True if the request user is the owner of the object, False otherwise
        '''
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        '''
        Returns a human-readable representation of the object's creation time.

        Args:
            obj: The object instance being serialized.

        Returns:
            str: A natural language representation of the creation time,
                such as "3 days ago".
        '''
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        '''
        Returns a human-readable representation of the object's last
            update time.

        Args:
            obj: The object instance being serialized.

        Returns:
            str: A natural language representation of the last update time,
                such as "2 hours ago".
        '''
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'post', 'created_at', 'updated_at', 'content'
        ]


class CommentDetailSerializer(CommentSerializer):
    '''
    Extends CommentSerializer to include additional details for a comment.

    Attributes:
        post (ReadOnlyField): The ID of the post associated with the comment.
    '''
    post = serializers.ReadOnlyField(source='post.id')
