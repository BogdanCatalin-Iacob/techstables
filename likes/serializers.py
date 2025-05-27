from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Like model, providing a read-only view of the owner's username.

    Attributes:
        owner (ReadOnlyField): The username of the user who liked the post.

    Meta:
        model (Model): The model class that is being serialized.
        fields (list): The fields to include in the serialized output.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = [
            'id', 'created_at', 'owner', 'post'
        ]
