from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from likes.models import Like
from comments.models import Comment


class PostDetailTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", password="pass1234")
        self.other = User.objects.create_user(
            username="other", password="pass1234")
        self.post = Post.objects.create(
            owner=self.owner, title="Owned", content="x")
        self.detail_url = f"/posts/{self.post.id}"

    def test_retrieve_post_detail_public(self):
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "Owned")
        # serializer exposes owner username
        self.assertEqual(resp.data["owner"], "owner")
        # counts should be present as read-only fields
        self.assertIn("comments_count", resp.data)
        self.assertIn("likes_count", resp.data)

    def test_only_owner_can_update(self):
        # non-owner
        self.client.login(username="other", password="pass1234")
        resp = self.client.put(
            self.detail_url, {"title": "new", "content": "c"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # owner
        self.client.logout()
        self.client.login(username="owner", password="pass1234")
        resp2 = self.client.patch(
            self.detail_url, {"content": "changed"}, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data["content"], "changed")

    def test_only_owner_can_delete(self):
        # non-owner cannot delete
        self.client.login(username="other", password="pass1234")
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # owner can delete
        self.client.logout()
        self.client.login(username="owner", password="pass1234")
        resp2 = self.client.delete(self.detail_url)
        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)

    def test_annotations_counts_reflect_likes_and_comments(self):
        # create interactions
        Comment.objects.create(owner=self.other, post=self.post, content="c1")
        Comment.objects.create(owner=self.owner, post=self.post, content="c2")
        Like.objects.create(owner=self.other, post=self.post)

        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["comments_count"], 2)
        self.assertEqual(resp.data["likes_count"], 1)

    def test_like_id_for_authenticated_user_on_detail(self):
        Like.objects.create(owner=self.owner, post=self.post)
        self.client.login(username="owner", password="pass1234")
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(resp.data.get("like_id"))
