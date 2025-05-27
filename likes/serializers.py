from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Like model, providing serialization and validation
    for Like instances, including a read-only view of the owner's username.

    Attributes:
        owner (ReadOnlyField): The username of the user who liked the post.

    Meta:
        model (Model): The model class that is being serialized.
        fields (list): The fields to include in the serialized output.

    Methods:
        create: Attempts to create a new Like instance, raising a validation
        error if a duplicate is detected.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = [
            'id', 'created_at', 'owner', 'post'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'details': 'possible duplicate'
            })
