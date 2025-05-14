from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .views import ProfileList


class ProfileListTests(APITestCase):
    def setUp(self):
        # Create test users
        User.objects.create_user(username='user1', password='pass1')
        User.objects.create_user(username='user2', password='pass2')

    def test_can_list_all_profiles(self):
        response = self.client.get('/profiles/')
        view = ProfileList()
        queryset = view.get_queryset()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(queryset.count(), 2)
