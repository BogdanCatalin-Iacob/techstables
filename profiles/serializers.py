from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Profile model, providing a JSON representation
    of profile instances. Includes fields for the profile's owner,
    timestamps, name, image, and a computed field to check if the
    requesting user is the owner of the profile.

    Attributes:
        owner (ReadOnlyField): The username of the profile's owner.
        is_owner (SerializerMethodField): Indicates if the requesting
            user is the owner of the profile.

    Methods:
        get_is_owner(obj): Determines if the requesting user is the
            owner of the profile instance.

    Meta:
        model (Profile): The model class to serialize.
        fields (list): The fields to include in the serialized output.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return obj.owner == request.user

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'image', 'is_owner'
        ]
