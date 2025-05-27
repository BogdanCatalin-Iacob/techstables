from rest_framework import generics, permissions
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    '''
    API view for listing and creating Follower instances.

    This view allows authenticated users to list all follower relationships
    or create a new one. The owner of the new follower relationship is set
    to the current user.

    Attributes:
        serializer_class (type): The serializer class used for
                                the Follower model.
        permission_classes (list): The permissions required to access
                                    this view.
        queryset (QuerySet): The queryset of Follower objects.

    Methods:
        perform_create(serializer): Saves a new Follower instance with the
        current user as the owner.
    '''
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.username)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    '''
    View for retrieving or deleting a Follower instance.

    This view allows users to retrieve or delete a specific follower
    relationship. It uses the FollowerSerializer to serialize the data
    and applies the IsOwnerOrReadOnly permission to ensure that only
    the owner of the follower relationship can delete it.
    '''
    serializer_class = FollowerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
