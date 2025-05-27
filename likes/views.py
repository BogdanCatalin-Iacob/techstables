from rest_framework import generics, permissions
from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    '''
    API view for listing and creating 'Like' instances.

    This view allows authenticated users to create new likes and
    provides a read-only list of all likes for unauthenticated users.

    Attributes:
        permission_classes (list): Specifies that the view is accessible
        to authenticated users for creating likes, while read-only access
        is available to others.
        serializer_class (LikeSerializer): The serializer class used for
        validating and serializing 'Like' instances.
        queryset (QuerySet): The base queryset for retrieving 'Like' objects.

    Methods:
        perform_create: Saves a new 'Like' instance with the current user
        as the owner.
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
