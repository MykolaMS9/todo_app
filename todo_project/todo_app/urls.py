from django.urls import path

from .views import (
    TodoListView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    HomeView,
)

"""
URL patterns for the Todo application views.

This list contains the URL routing configuration for the Todo application, 
mapping URLs to corresponding views that allow users to view, create, update, 
and delete their Todo items. 

Path Definitions:
1. **home**:
    - Path: "/home"
    - View: `HomeView.as_view()`
    - Template: "todo/home.html"
    - Purpose: Renders the home page (HomeView).
2. **main**:
    - Path: ""
    - View: `TodoListView.as_view()`
    - Template: "todo/list.html"
    - Purpose: Displays the list of Todo items for the authenticated user (TodoListView).
3. **create**:
    - Path: "/todo/create"
    - View: `TodoCreateView.as_view()`
    - Template: "todo/create.html"
    - Purpose: Allows the creation of a new Todo item (TodoCreateView).
4. **edit**:
    - Path: "/todo/edit/<pk>"
    - View: `TodoUpdateView.as_view()`
    - Template: "todo/update.html"
    - Purpose: Allows editing an existing Todo item by its primary key (TodoUpdateView).
5. **delete**:
    - Path: "/todo/delete/<pk>"
    - View: `TodoDeleteView.as_view()`
    - Template: "todo/delete.html"
    - Purpose: Allows deleting a Todo item by its primary key (TodoDeleteView).
"""
urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    path("", TodoListView.as_view(), name="main"),
    path("todo/create", TodoCreateView.as_view(), name="create_todo"),
    path("todo/edit/<pk>", TodoUpdateView.as_view(), name="edit_todo"),
    path("todo/delete/<pk>", TodoDeleteView.as_view(), name="delete_todo"),
]
