from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Post model, providing fields for owner details,
    timestamps, and content. Includes a method to determine if the current
    user is the owner of the post. Fields include owner username, profile ID,
    profile image URL, and a boolean indicating ownership.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return obj.owner == request.user

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image'
        ]
