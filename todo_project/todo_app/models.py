from django.conf import settings
from django.db import models

# Create your models here.


class Todo(models.Model):
    """
    Represents a Todo item in the application.

    This model stores a user's Todo task, including details like the title,
    description, completion status, and the user associated with the task.

    Attributes:
        title (CharField): The title of the Todo item, with a maximum length of 50 characters.
        description (CharField): A description of the Todo item, with a maximum length of 300 characters.
        completed (BooleanField): A boolean flag indicating whether the Todo item is completed. Defaults to False.
        published (DateTimeField): The timestamp of when the Todo item was created. Automatically set to the current time.
        user (ForeignKey): A foreign key linking the Todo item to a specific user. The user is required and the relationship is set to cascade on delete.

    Methods:
        __str__(): Returns a string representation of the Todo instance, typically the title of the task.

    Example:
        todo = Todo.objects.create(title="My Todo", description="Task description", user=user)
        todo.completed = True
        todo.save()
    """

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=False)
    completed = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title


class UserSettings(models.Model):
    """
    Represents the settings for a user in the Todo application.

    This model stores user-specific settings, including the number of Todo items
    to display per page in the Todo list. Each user has a unique `UserSettings` object
    associated with them, which is created when the user registers.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the `User` model.
                              It ensures that each user has a unique set of settings.
        cards_per_page (IntegerField): The number of Todo items to display per page.
                                       Defaults to 9 if not specified by the user.

    Methods:
        __str__(): Returns a string representation of the `UserSettings` instance,
                   displaying the associated user.

    Example:
        user_settings = UserSettings.objects.get(user=user)
        user_settings.cards_per_page  # Access the cards per page for a user.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cards_per_page = models.IntegerField(default=9)

    def __str__(self):
        return self.user
