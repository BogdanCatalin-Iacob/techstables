from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Post model, providing serialization and validation
    for post data. It includes fields for owner details, timestamps, and
    content, and implements a method to check if the current user is the
    owner of the post. The serializer also validates image size and dimensions.

    Attributes:
        owner (ReadOnlyField): The username of the post owner.
        profile_id (ReadOnlyField): The ID of the owner's profile.
        profile_image (ReadOnlyField): The URL of the owner's profile image.
        is_owner (SerializerMethodField): Boolean indicating if the current
            user is the owner of the post.

    Methods:
        validate_image(value): Validates the size and dimensions of the image.
        get_is_owner(obj): Returns if the current user is the owner of the post

    Meta:
        model (Model): The Post model.
        fields (list): List of fields to be serialized.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image larger than 2MB!'
            )
        if value.height > 4096:
            raise serializers.ValidationError(
                'Image height is larger than 4096 pixels'
            )
        if value.width > 4096:
            serializers.ValidationError(
                'Image width is larger than 4096 pixels'
            )

    def get_is_owner(self, obj):
        request = self.context['request']
        return obj.owner == request.user

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image'
        ]
