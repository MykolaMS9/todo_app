from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserSettings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_settings(sender, instance, created, **kwargs):
    """
    Signal receiver to create UserSettings when a new user is created.

    This receiver listens for the `post_save` signal emitted after a user instance
    is saved. If the user instance is newly created, it creates a corresponding
    `UserSettings` object for the user. This ensures that every new user has
    default settings stored in the `UserSettings` model.

    Args:
        sender (Model): The model class that triggered the signal, which is `AUTH_USER_MODEL`.
        instance (User): The actual user instance that was saved.
        created (bool): A flag that indicates whether the user instance was created.
        **kwargs: Additional keyword arguments passed by the signal.

    Side Effects:
        - Creates a new `UserSettings` instance associated with the newly created user.
    """
    if created:
        UserSettings.objects.create(user=instance)
