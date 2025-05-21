from rest_framework import generics, permissions
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    '''
    API view for listing and creating Post instances.

    This view allows authenticated users to create new posts and
    provides a read-only list of all posts to unauthenticated users.
    Utilizes the PostSerializer for serialization and enforces
    permissions using IsAuthenticatedOrReadOnly.
    '''
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    API view for retrieving, updating, or deleting a Post instance.

    This view allows users to retrieve, update, or delete a specific post
    instance. It uses the PostSerializer for serialization and enforces
    permissions such that only the owner of the post can modify or delete it.

    Attributes:
        serializer_class (PostSerializer): The serializer class used for the Post model.
        permission_classes (list): List containing the permission class IsOwnerOrReadOnly.
        queryset (QuerySet): The queryset used to retrieve Post instances.
    '''
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
