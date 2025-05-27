from rest_framework import generics, permissions
from techstables_backend.permissions import IsOwnerOrReadOnly
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


class LikeDetail(generics.RetrieveDestroyAPIView):
    '''
    API view for retrieving and deleting a Like instance.

    This view allows users to retrieve details of a specific Like
    instance or delete it if they are the owner. It uses the
    IsOwnerOrReadOnly permission to ensure that only the owner
    can delete the Like.

    Attributes:
        permission_classes (list): Specifies the permission class
            to check if the user is the owner or if the request
            method is safe.
        serializer_class (LikeSerializer): The serializer class
            used to serialize and validate Like instances.
        queryset (QuerySet): The queryset that retrieves all Like
            instances from the database.
    '''
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
