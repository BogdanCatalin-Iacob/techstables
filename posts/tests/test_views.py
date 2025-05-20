from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from posts.models import Post


class PostListTest(APITestCase):
    def setUp(self):
        Post.objects.create(
            owner=User.objects.create(username='test1', password='password'),
            title='Test Post 1',
            content='Content 1')

    def test_unauthenticated_users_can_retrieve_posts_list(self):
        response = self.client.get('/posts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post 1')
