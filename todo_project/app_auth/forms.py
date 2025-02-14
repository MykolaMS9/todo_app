from django.forms import (
    CharField,
    TextInput,
    EmailInput,
    EmailField,
    PasswordInput,
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser


class RegisterForm(UserCreationForm):
    """
    A form for creating a new user account (registration).

    This form inherits from `UserCreationForm` and adds fields for username, email, and password
    to handle user registration. It includes validation for the username, email, and matching passwords.

    Attributes:
        username (CharField): The username of the user, required and with a minimum length of 3 and maximum length of 16 characters.
        email (EmailField): The email address of the user, required and with a maximum length of 30 characters.
        password1 (CharField): The first password field, required, and displayed using a password input widget.
        password2 (CharField): The second password field, required, used to confirm the password. It must match `password1`.

    Methods:
        __init__(): Initializes the form with customized widgets for better styling.
        clean_password2(): Validates that the passwords match and that password1 is not empty.

    Example:
        - GET request: Displays the registration form for the user.
        - POST request: Handles the form submission, validates the data, and creates the new user if valid.

    Meta:
        - Inherits from `UserCreationForm`, which includes basic functionality for creating a user and checking the password.
    """

    username = CharField(
        max_length=16,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    email = EmailField(
        max_length=30, required=True, widget=EmailInput(attrs={"class": "form-control"})
    )
    password1 = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )
    password2 = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    """
    A form for user authentication (login).

    This form inherits from `AuthenticationForm` and provides fields for username and password
    to authenticate a user. It validates that the provided credentials are correct and allows
    the user to log in to the application.

    Attributes:
        username (CharField): The username of the user, required and with a minimum length of 3 and maximum length of 16 characters.
        password (CharField): The password of the user, required, and displayed using a password input field.

    Meta:
        - The form inherits from `AuthenticationForm`, which handles the actual user authentication logic.

    Example:
        - GET request: Displays the login form for the user.
        - POST request: Handles the login submission and validates the credentials.

    Methods:
        __init__(): Initializes the form, customizing widget attributes for better styling.
    """

    username = CharField(
        max_length=16,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    password = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "password")
