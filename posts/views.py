from django.db.models import Count
from rest_framework import generics, permissions, filters
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    '''
    API view for listing and creating Post instances.

    This view allows authenticated users to create new posts and
    provides a list of existing posts. Posts are annotated with
    the count of comments and likes, and can be ordered by these
    counts or the creation date of likes.

    Attributes:
        serializer_class (PostSerializer): The serializer class used for
            validating and serializing post data.
        permission_classes (list): Permissions required to access the view.
        queryset (QuerySet): The base queryset for retrieving posts, annotated
            with comment and like counts.
        filter_backends (list): Filters applied to the queryset.
        ordering_fields (list): Fields available for ordering the queryset.

    Methods:
        perform_create(serializer): Saves a new post instance with the
            current user as the owner.
    '''
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'commnets__count',
        'likes__count',
        'likes__created_at'
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
    queryset = Post.objects.all()
