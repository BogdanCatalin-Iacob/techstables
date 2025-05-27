from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Profile model, converting profile instances into
    JSON format. It includes fields for the profile's owner, timestamps,
    name, image, and additional computed fields to determine ownership
    and following status.

    Attributes:
        owner (ReadOnlyField): The username of the profile's owner.
        is_owner (SerializerMethodField): Indicates if the requesting
            user is the owner of the profile.
        following_id (SerializerMethodField): The ID of the follower
            relationship if the requesting user follows the profile owner.
        posts_count (ReadOnlyField): The number of posts created by user.
        followers_count (ReadOnlyField): The number of followers a user has.
        following_count (ReadOnlyField): The number of users followed by user.

    Methods:
        get_is_owner(obj): Checks if the requesting user is the owner
            of the profile instance.
        get_following_id(obj): Retrieves the ID of the follower
            relationship if it exists.

    Meta:
        model (Profile): The model class to serialize.
        fields (list): The fields to include in the serialized output.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        '''
         Determines if the requesting user is the owner of the profile instance
        being serialized.

        Parameters:
            obj: The profile instance being serialized.

        Returns:
            bool: True if the requesting user is the owner of the profile,
            otherwise False.
        '''
        request = self.context['request']
        return obj.owner == request.user

    def get_following_id(self, obj):
        '''
        Retrieves the ID of the follower relationship between the authenticated
        user and the owner of the profile instance being serialized.

        Parameters:
            obj: The profile instance being serialized.

        Returns:
            int or None: The ID of the follower relationship if it exists,
            otherwise None.
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        '''
        Configuration for the Profile serializer, specifying the model
        and fields to include in the serialized output.

        Attributes:
            model (Profile): The model class to serialize.
            fields (list): The fields to include in the serialized output,
            including the profile's ID, owner, timestamps, name, image,
            and additional computed fields for ownership and following status.
        '''
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count'
        ]
