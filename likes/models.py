from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Like(models.Model):
    '''
    Represents a 'Like' entity that associates a 'User' with a 'Post'.

    Attributes:
        owner (ForeignKey): A reference to the User who liked the post.
        post (ForeignKey): A reference to the Post that is liked.
        created_at (DateTimeField): The timestamp when the like was created.

    Meta:
        ordering: Orders the likes by creation date in descending order.
        unique_together: Ensures that a user can like a specific post only once.

    Methods:
        __str__: Returns a string representation of the like,
        showing the owner and the post.
    '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'post']

    def __str__(self):
        return f'{self.owner} {self.post}'
