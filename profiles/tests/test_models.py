from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..models import Profile
import time


class ProfileModelTests(APITestCase):
    def test_auto_created_profile_on_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        # The signal should create profile automatically
        profile = Profile.objects.get(owner=user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.owner, user)

    def test_no_duplicate_profiles_on_user_update(self):
        user = User.objects.create_user(username='testuser2', password='testpass')
        # Saving user again should not create another profile
        user.first_name = 'Bogdan'
        user.save()
        self.assertEqual(Profile.objects.filter(owner=user).count(), 1)

    def test_str_representation(self):
        user = User.objects.create_user(username='testuser3', password='testpass')
        profile = Profile.objects.get(owner=user)
        self.assertEqual(str(profile), f'{user}\'s profile')

    def test_default_image_upload(self):
        user = User.objects.create_user(username='testuser4', password='testpass')
        profile = Profile.objects.get(owner=user)
        # Default image should be set to the configured default path
        self.assertEqual(profile.image.name, '../default_profile_xdfle7')

    def test_ordering_by_profile_desc(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        time.sleep(0.01)  # Ensure created_at differs
        user2 = User.objects.create_user(username='user2', password='pass')

        profiles = list(Profile.objects.all())  # Meta ordering is ['-created_at']
        self.assertEqual(profiles[0].owner, user2)
        self.assertEqual(profiles[1].owner, user1)

def test_updated_change_on_save(self):
    pass

def test_delete_user_deletes_profile(self):
    pass

def test_cannot_create_profile_for_the_same_user_twice(self):
    pass