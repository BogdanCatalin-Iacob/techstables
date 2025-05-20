from rest_framework import generics, permissions
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
