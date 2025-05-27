from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Follower model, providing a read-only view of the
    owner's and followed user's usernames.

    Attributes:
        owner (ReadOnlyField): The username of the user who is following.
        followed_name (ReadOnlyField): The username of the user being followed.

    Meta:
        model (Model): The model associated with this serializer.
        fields (list): The fields to be serialized.

    Methods:
        create(validated_data): Creates a new Follower instance, handling
        potential IntegrityError exceptions to prevent duplicate entries.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = [
            'id', 'owner', 'created_at', 'followed', 'followed_name',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'details': 'possible duplicate'
            })
