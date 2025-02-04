from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages  # flesh messages

from .forms import RegisterForm


# Create your views here.


class RegisterView(View):
    """
    A view for handling user registration.

    This view provides functionality for displaying a user registration form,
    handling POST requests to create a new user, and redirecting to the appropriate
    page after successful or unsuccessful form submission.

    Attributes:
        template_name (str): The path to the registration template (app_auth/register.html).
        from_class (form): The form class used to validate and save the registration data (RegisterForm).

    Methods:
        dispatch(request, *args, **kwargs): Handles the request and redirects to a different page if the user is already authenticated.
        get(request): Renders the registration page with the registration form.
        post(request): Handles form submission, saves the new user if the form is valid, and redirects to the signin page.

    Example:
        - GET request: Renders the registration form for new users to fill out.
        - POST request: Validates the form and creates a new user. On success, redirects to the signin page.
    """

    template_name = "app_auth/register.html"
    from_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user is already authenticated before handling the request.

        If the user is authenticated, they are redirected to the 'pictures' page.
        Otherwise, the request is passed to the next handler (usually the `get` or `post` method).

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional arguments passed to the dispatch method.
            **kwargs: Additional keyword arguments passed to the dispatch method.

        Returns:
            HttpResponse: A redirect response if the user is authenticated,
                           or the result of the `super().dispatch()` method if not.
        """
        if request.user.is_authenticated:
            return redirect(to="app_photo:pictures")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        Renders the registration form when the user makes a GET request.

        Args:
            request (HttpRequest): The HTTP GET request object.

        Returns:
            HttpResponse: The rendered registration form template.
        """
        return render(request, self.template_name, {"form": self.from_class})

    def post(self, request):
        """
        Handles the form submission when the user makes a POST request.

        If the registration form is valid, a new user is created, and the user is
        redirected to the signin page. If the form is invalid, it is re-rendered
        with error messages.

        Args:
            request (HttpRequest): The HTTP POST request object containing the form data.

        Returns:
            HttpResponse: A redirect to the signin page if the form is valid,
                           or a re-render of the registration form with validation errors.
        """
        form = self.from_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Success! Account created for {username}!")
            return redirect(to="app_auth:signin")
        return render(request, self.template_name, {"form": form})
