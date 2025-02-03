from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
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
