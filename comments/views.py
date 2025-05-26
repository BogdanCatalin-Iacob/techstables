from rest_framework import generics, permissions
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):
    '''
    API view for listing and creating comments.

    This view provides a list of all comments and allows authenticated users
    to create new comments. It uses the CommentSerializer for serialization
    and enforces permissions such that only authenticated users can create
    comments, while others can only read.

    Attributes:
        serializer_class (CommentSerializer): The serializer used for the comments.
        permission_classes (list): Permissions required to access the view.
        queryset (QuerySet): The base queryset for retrieving comments.

    Methods:
        perform_create(serializer): Saves a new comment with the current user as the owner.
    '''
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    API view for retrieving, updating, or deleting a comment instance.

    Uses CommentDetailSerializer for serialization and IsOwnerOrReadOnly
    for permission control. Operates on the Comment model.
    '''
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
