from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    A custom user model that extends the default Django User model.

    This model adds an `email` field to the standard user model and ensures that
    the email is unique for each user. It inherits from `AbstractUser`, which provides
    the standard authentication fields (username, password, first_name, last_name, etc.)

    Attributes:
        email (EmailField): The email address of the user. This field is required to be unique.

    Methods:
        __str__(): Returns a string representation of the user, typically the username.

    Example:
        user = CustomUser.objects.create_user(username="john_doe", email="john@example.com", password="password123")
        print(user.email)  # Outputs: john@example.com
    """

    email = models.EmailField(unique=True)
