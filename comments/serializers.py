from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Comment model, providing fields for comment details
    and additional user-related information.

    Attributes:
        owner (ReadOnlyField): The username of the comment owner.
        is_owner (SerializerMethodField): Indicates if the request user is the owner.
        profile_id (ReadOnlyField): The ID of the owner's profile.
        profile_image (ReadOnlyField): The URL of the owner's profile image.

    Methods:
        get_is_owner(obj): Determines if the request user is the owner of the comment.

    Meta:
        model (Comment): The model that is being serialized.
        fields (list): The fields to be included in the serialized output.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

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
