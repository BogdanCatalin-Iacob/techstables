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
    pass

def test_profile_deletion_on_user_deletion(self):
    pass

def test_str_representation_of_profile(self):
    pass

def test_default_image_upload(self):
    pass

def test_ordering_by_profile_desc(self):
    pass

def test_updated_change_on_save(self):
    pass

def test_delete_user_deletes_profile(self):
    pass

def test_cannot_create_profile_for_the_same_user_twice(self):
    pass