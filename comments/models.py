from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    '''
    A model representing a comment on a post.

    Attributes:
        owner (ForeignKey): A reference to the User who created the comment.
        post (ForeignKey): A reference to the Post that the comment
                            is associated with.
        created_at (DateTimeField): The date and time when
                                    the comment was created.
        updated_at (DateTimeField): The date and time when
                                    the comment was last updated.
        content (TextField): The text content of the comment.

    Meta:
        ordering (list): Orders comments by creation date in descending order.

    Methods:
        __str__(): Returns a string representation of the comment content.
    '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
