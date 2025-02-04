from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    """
    A form for creating and updating Todo items.

    This form provides a user interface for adding and editing Todo tasks. It includes
    fields for the task title and description. The form is associated with the `Todo` model
    and ensures that only the specified fields (`title` and `description`) are used in the form.

    Attributes:
        title (CharField): The title of the Todo item. It uses a `TextInput` widget with `form-control` class.
        description (CharField): The description of the Todo item. It uses a `Textarea` widget with `form-control` class.

    Meta:
        model (Model): The model associated with the form (`Todo`).
        fields (tuple): The fields of the `Todo` model to be included in the form (`title` and `description`).

    Example:
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new or updated Todo item
    """

    title = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        max_length=250, widget=forms.Textarea(attrs={"class": "form-control"})
    )

    class Meta:
        model = Todo
        fields = ("title", "description")


class TodoUpdateForm(TodoForm):

    completed = forms.BooleanField(
        label="Check if this task is finished",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )

    class Meta(TodoForm.Meta):
        fields = TodoForm.Meta.fields + ("completed",)
