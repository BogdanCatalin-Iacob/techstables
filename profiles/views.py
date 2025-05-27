from django.db.models import Count
from rest_framework import generics, filters
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    '''
    API view to list all Profile instances with annotated counts.

    This view provides a list of all Profile instances, annotated with
    counts for posts, followers, and following relationships. The
    ProfileSerializer is used to convert Profile model instances into
    JSON format for API responses. Supports ordering by various fields
    including posts count, followers count, and following count.

    Attributes:
        queryset (QuerySet): Annotated Profile instances ordered by
            creation date.
        serializer_class (ProfileSerializer): Serializer class for
            Profile instances.
        filter_backends (list): List of filter backends for ordering.
        ordering_fields (list): Fields available for ordering the
            results.
    '''
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
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
