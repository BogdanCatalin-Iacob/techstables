from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    '''
    API view for listing and creating Post instances.

    This view supports filtering, searching, and ordering of posts based on
    various fields such as comments count, likes count, and creation date.
    Authenticated users can create new posts, while read-only access is
    granted to unauthenticated users.

    Attributes:
        serializer_class (PostSerializer): The serializer class used for
            serializing Post instances.
        permission_classes (list): Permissions required to access the view.
        queryset (QuerySet): The base queryset for retrieving Post instances,
            annotated with comments and likes counts.
        filter_backends (list): The list of filter backends used for
            filtering, searching, and ordering.
        ordering_fields (list): Fields available for ordering the results.
        filterset_fields (list): Fields available for filtering the results.
        search_fields (list): Fields available for searching the results.

    Methods:
        perform_create: Saves a new Post instance with the current user as
            the owner.
    '''
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    ordering_fields = [
        'comments__count',
        'likes__count',
        'likes__created_at'
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile'
    ]
    search_fields = [
        'owner__username',
        'title'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    API view for retrieving, updating, or deleting a Post instance.

    This view allows users to retrieve, update, or delete a specific post
    instance. It uses the PostSerializer for serialization and enforces
    permissions such that only the owner of the post can modify or delete it.

    Attributes:
        serializer_class (PostSerializer): The serializer class used
            for the Post model.
        permission_classes (list): List containing the permission
            class IsOwnerOrReadOnly.
        queryset (QuerySet): The queryset used to retrieve Post instances.
    '''
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
