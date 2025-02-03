from django.urls import path

from .views import (
    TodoListView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    HomeView,
)

urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    path("", TodoListView.as_view(), name="main"),
    path("todo/create", TodoCreateView.as_view(), name="create_todo"),
    path("todo/edit/<pk>", TodoUpdateView.as_view(), name="edit_todo"),
    path("todo/delete/<pk>", TodoDeleteView.as_view(), name="delete_todo"),
]
