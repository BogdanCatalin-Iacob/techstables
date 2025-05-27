from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):
    '''
    API view for listing and creating comments.

    This view allows authenticated users to list all comments or
        create a new comment.
    Comments can be filtered by the associated post. The owner of a
        new comment is
    automatically set to the current user.

    Attributes:
        serializer_class (CommentSerializer): The serializer class used
            for the comments.
        permission_classes (list): Permissions required to access the view.
        queryset (QuerySet): The base queryset for retrieving comments.
        filter_backends (list): The backends used for filtering the queryset.
        filterset_fields (list): The fields that can be used to filter
            the queryset.

    Methods:
        perform_create(serializer): Saves a new comment with the current user
            as the owner.
    '''
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'post'
    ]

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
