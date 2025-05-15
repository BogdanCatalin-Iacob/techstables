from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from ..views import ProfileList, ProfileDetail
from ..models import Profile


class ProfileListTests(APITestCase):
    def setUp(self):
        # Create test users
        User.objects.create_user(username='user1', password='pass1')
        User.objects.create_user(username='user2', password='pass2')

    def test_can_list_all_profiles(self):
        factory = APIRequestFactory()
        request = factory.get('/profiles/')
        view = ProfileList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


class ProfileDetailTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='user1', password='pass1')

    def test_logged_out_user_cant_edit_profile(self):
        profile = Profile.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.post(f'/profiles/{profile.id}', {'name': 'Nick'})
        view = ProfileDetail.as_view()

        response = view(request, pk=1)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_retrieve_profile_using_valid_id(self):
        profile = Profile.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.get(f'/profiles/{profile.id}/')
        view = ProfileDetail.as_view()
        response = view(request, pk=profile.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_profile(self):
        factory = APIRequestFactory()
        request = factory.get('/profiles/9999/')
        view = ProfileDetail.as_view()
        response = view(request, pk=9999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
