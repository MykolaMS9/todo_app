from django.conf import settings
from django.db import models

# Create your models here.


class Todo(models.Model):
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
