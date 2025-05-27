from rest_framework import generics
from techstables_backend.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    '''
    API view to list all Profile instances.

    Uses the ProfileSerializer to convert Profile model instances
    into JSON format for API responses.
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
