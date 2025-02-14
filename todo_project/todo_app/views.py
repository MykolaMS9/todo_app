from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from .forms import TodoForm, TodoUpdateForm
from .models import Todo, UserSettings
from .repository import set_cards_per_page


# Create your views here.


class HomeView(ListView):
    """
    A view for rendering the home page.

    This view renders the home page of the application. It is a simple ListView
    that does not use any specific model or queryset and only renders the
    `home.html` template.

    Attributes:
        template_name (str): The name of the template to render, `todo/home.html`.
        success_url (str): The URL to redirect to upon successful operation, which is
                            the main page (`reverse_lazy("main")`).

    Methods:
        get(request, *args, **kwargs): Override of the default `get` method to
                                       render the `home.html` template.
    """

    template_name = "todo/home.html"
    success_url = reverse_lazy("main")

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and renders the home page.

        Args:
            request (HttpRequest): The incoming request.
            *args: Additional arguments.
            **kwargs: Keyword arguments.

        Returns:
            HttpResponse: The rendered home page template.
        """
        return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class TodoListView(LoginRequiredMixin, ListView):
    """
    A view for listing Todo items for an authenticated user.

    This view allows an authenticated user to see their Todo items,
    with pagination based on the number of items per page specified in their settings.
    The `cards_per_page` is fetched from the `UserSettings` model and used for pagination.

    Attributes:
        model (models.Model): The model that the view interacts with, which is `Todo`.
        template_name (str): The name of the template to render, `todo/list.html`.
        success_url (str): The URL to redirect to after successful operations, which is
                            the main page (`reverse_lazy("main")`).
        context_object_name (str): The name of the context variable to use in the template, which is `todo_list`.
        form_class (forms.Form): The form class used to filter or create Todo items (`TodoForm`).
        cards_per_page (int): The number of Todo items to display per page (fetched from user settings).

    Methods:
        get_queryset(): Returns a queryset of Todo items filtered by the current logged-in user.
        get_data(): Retrieves the number of items per page from the GET request or user settings.
        get_paginate_by(queryset): Returns the number of items to display per page for pagination.
        get_context_data(object_list=None, **kwargs): Adds additional context (`cards_per_page`) to the template.
    """

    model = Todo
    template_name = "todo/list.html"
    success_url = reverse_lazy("main")
    context_object_name = "todo_list"
    form_class = TodoForm
    cards_per_page = None

    def get_queryset(self):
        """
        Returns a queryset of Todo items for the current logged-in user.

        This method fetches the `cards_per_page` setting from the `UserSettings` model
        and filters the `Todo` items by the current user.

        Returns:
            QuerySet: A queryset of `Todo` items for the logged-in user.
        """
        self.cards_per_page = UserSettings.objects.get(
            user=self.request.user
        ).cards_per_page
        return Todo.objects.filter(user=self.request.user)

    def get_data(self):
        """
        Retrieves the number of items per page from the GET request or user settings.

        This method reads the `cards_per_page` from the GET parameters or defaults to
        the value stored in the user settings. If the provided value is invalid, it
        falls back to the default value.

        Returns:
            int: The number of items to display per page.
        """
        cards_per_page_request = self.request.GET.get(
            "cards_per_page", self.cards_per_page
        )
        try:
            cards_per_page_request = int(cards_per_page_request)
            if cards_per_page_request < 1:
                raise ValueError
        except ValueError:
            cards_per_page_request = self.cards_per_page
        return cards_per_page_request

    def get_paginate_by(self, queryset):
        """
        Returns the number of items to display per page for pagination.

        This method is used by Django to determine the number of items displayed per
        page in the paginated list of `Todo` items. It fetches the value from the GET
        request or uses the user settings.

        Args:
            queryset (QuerySet): The queryset to paginate.

        Returns:
            int: The number of items to display per page.
        """
        self.cards_per_page = self.get_data()
        set_cards_per_page(self.request.user, self.cards_per_page)
        return self.cards_per_page

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Adds additional context to the template.

        This method adds the `cards_per_page` value to the context, so it can be
        used in the template to display the number of items per page.

        Args:
            object_list (QuerySet): A list of the objects being paginated.
            **kwargs: Additional context data.

        Returns:
            dict: A dictionary containing the context data, including `cards_per_page`.
        """
        context = super().get_context_data(**kwargs)
        context["cards_per_page"] = self.cards_per_page
        return context


@method_decorator(login_required, name="dispatch")
class TodoCreateView(CreateView):
    """
    A view for creating a new Todo item.

    This view allows authenticated users to create a new Todo item using a form.
    The form is automatically populated with the current user, ensuring that
    the Todo item is associated with the logged-in user.

    Attributes:
        model (models.Model): The model that the view interacts with, which is `Todo`.
        template_name (str): The name of the template to render, `todo/create.html`.
        form_class (forms.Form): The form class used to create a new Todo item (`TodoForm`).
        success_url (str): The URL to redirect to after the form is successfully submitted,
                            which is the main page (`reverse_lazy("main")`).

    Methods:
        form_valid(form): Override of `form_valid` method to set the user as the
                          current logged-in user when the form is valid.
    """

    model = Todo
    template_name = "todo/create.html"
    form_class = TodoForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        """
        Override the form_valid method to associate the current user with the
        Todo item being created.

        Args:
            form (forms.Form): The form with validated data.

        Returns:
            HttpResponseRedirect: A redirect to the `success_url` after the form is successfully submitted.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TodoUpdateView(UpdateView):
    model = Todo
    template_name = "todo/update.html"
    form_class = TodoUpdateForm
    success_url = reverse_lazy("main")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied(
                "Forbidden. You you have no permission to update this todo."
            )
        return obj


@method_decorator(login_required, name="dispatch")
class TodoDeleteView(DeleteView):
    """
    A view for updating a Todo item for an authenticated user.

    This view allows an authenticated user to update an existing Todo item.
    Only the user who created the Todo item is allowed to update it. If any other
    user tries to update the Todo item, a `PermissionDenied` error will be raised.

    Attributes:
        model (models.Model): The model that the view interacts with, which is `Todo`.
        template_name (str): The name of the template to render, `todo/update.html`.
        form_class (forms.Form): The form class used to update an existing Todo item (`TodoUpdateForm`).
        success_url (str): The URL to redirect to after the form is successfully submitted,
                            which is the main page (`reverse_lazy("main")`).

    Methods:
        get_queryset(): Returns a queryset of Todo items filtered by the current logged-in user.
        get_object(queryset=None): Retrieves the Todo item and checks if the current user is the owner.
    """

    model = Todo
    template_name = "todo/delete.html"
    success_url = reverse_lazy("main")

    def get_queryset(self):
        """
        Returns a queryset of Todo items for the current logged-in user.

        This method filters the Todo items to only include those belonging to
        the current user.

        Returns:
            QuerySet: A queryset of `Todo` items for the logged-in user.
        """
        return Todo.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        """
        Retrieves the Todo item to be updated and ensures the current user is the owner.

        This method checks whether the Todo item belongs to the current user. If the user
        does not own the item, a `PermissionDenied` error is raised to prevent unauthorized access.

        Args:
            queryset (QuerySet, optional): A queryset to filter the Todo items.

        Returns:
            Todo: The `Todo` item to be updated.

        Raises:
            PermissionDenied: If the user does not have permission to update the item.
        """
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied(
                "Forbidden. You you have no permission to update this todo."
            )
        return obj
