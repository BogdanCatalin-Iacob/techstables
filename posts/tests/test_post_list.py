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
