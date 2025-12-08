from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post


class PostListTests(APITestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username="alice", password="pass1234")
        self.user2 = User.objects.create_user(username="bob", password="pass1234")

        # Posts
        self.p1 = Post.objects.create(owner=self.user1, title="Alpha", content="content a")
        self.p2 = Post.objects.create(owner=self.user2, title="Beta", content="content b")

        self.list_url = "/posts/"  # configured in posts/urls.py

    def test_list_posts_is_public_readonly(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # ensure results returned and ordering by -created_at (newest first)
        ids = [item["id"] for item in resp.data["results"]] if isinstance(resp.data, dict) and "results" in resp.data else [item["id"] for item in resp.data]
        self.assertEqual(ids, [self.p2.id, self.p1.id])

    def test_create_requires_authentication(self):
        payload = {"title": "Gamma", "content": "c"}
        resp = self.client.post(self.list_url, payload)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_post_owner_set(self):
        self.client.login(username="alice", password="pass1234")
        payload = {"title": "Gamma", "content": "c"}
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["owner"], "alice")
        self.assertEqual(Post.objects.count(), 3)
        self.assertTrue(Post.objects.filter(title="Gamma", owner=self.user1).exists())

    def test_search_by_title(self):
        resp = self.client.get(self.list_url, {"search": "Alpha"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.data["results"] if isinstance(resp.data, dict) and "results" in resp.data else resp.data
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Alpha")

    def test_ordering_by_likes_count_field_is_accepted(self):
        # Ensure that the view accepts ordering fields defined
        resp = self.client.get(self.list_url, {"ordering": "likes__count"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unique_title_validation(self):
        self.client.login(username="bob", password="pass1234")
        # Duplicate title should fail because Post.title is unique
        resp = self.client.post(self.list_url, {"title": "Alpha", "content": "dup"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", resp.data)

    def test_search_by_owner_username(self):
        resp = self.client.get(self.list_url, {"search": "bob"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.data["results"] if isinstance(resp.data, dict) and "results" in resp.data else resp.data
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["owner"], "bob")

    def test_ordering_by_created_at_desc_default(self):
        # default queryset ordering is -created_at
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.data["results"] if isinstance(resp.data, dict) and "results" in resp.data else resp.data
        self.assertGreaterEqual(items[0]["created_at"], items[1]["created_at"])

    def test_like_id_present_for_authenticated_user(self):
        # When authenticated, like_id field should be present (None if no like)
        self.client.login(username="alice", password="pass1234")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.data["results"] if isinstance(resp.data, dict) and "results" in resp.data else resp.data
        # Ensure key exists and is None by default
        self.assertIn("like_id", items[0])
