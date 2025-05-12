from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Represents a user profile associated with a Django User model.

    Attributes:
        owner (User):
            A one-to-one relationship with the User model,
            indicating the profile's owner.

        created_at (DateTimeField):
            Timestamp of when the profile was created,
            automatically set.

        updated_at (DateTimeField):
            Timestamp of the last update to the profile,
            automatically set.

        name (CharField):
            Optional name of the profile owner,
            with a maximum length of 100 characters.

        image (ImageField):
            Profile image, stored in the 'images/' directory,
            with a default image.

    Methods:
        __str__():
            Returns a string representation of the profile,
            including the owner's username.

    Meta:
        ordering:
            Orders profiles by creation date in descending order.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', default='media/images/default_profile_xdfle7')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function that creates a Profile instance
    whenever a new User instance is created.

    Args:
        sender (type): The model class that sent the signal.
        instance (User): The instance of the User model that was created.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
