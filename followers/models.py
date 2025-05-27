from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    '''
    Represents a follower relationship between two users.

    Attributes:
        owner (User): The user who is following another user.
        followed (User): The user being followed.
        created_at (datetime): The date and time when the follow relationship
                                was created.

    Meta:
        ordering (list): Orders the follower relationships by creation date
                        in descending order.
        unique_together (list): Ensures that each follower-followed pair is
                                unique.

    Methods:
        __str__(): Returns a string representation of the
                    follower relationship.
    '''
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f'{self.owner} {self.followed}'
