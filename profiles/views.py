from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    '''
    API view for listing profiles with annotated counts for posts, followers,
    and following. Supports ordering and filtering based on specified fields.

    Attributes:
        queryset (QuerySet): Annotated queryset of profiles
            ordered by creation date.
        serializer_class (ProfileSerializer):
            Serializer class for profile data.
        filter_backends (list): List of filter backends for ordering
            and filtering.
        filterset_fields (list): Fields available for filtering profiles.
        ordering_fields (list): Fields available for ordering profiles.
    '''
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__following__followed__profile'
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'followed_count',
        'owner__following__created_at',
        'owner__followed__created_at'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    '''
    API view for retrieving and updating a Profile instance.

    This view allows users to retrieve and update their own profile
    information. It uses the ProfileSerializer to serialize profile
    data and applies the IsOwnerOrReadOnly permission to ensure that
    only the profile owner can update the profile.

    Attributes:
        queryset (QuerySet): A queryset of all Profile instances.
        serializer_class (type): The serializer class used for
            serializing profile data.
        permission_classes (list): A list of permission classes
            applied to the view.
    '''
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
