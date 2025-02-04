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
    template_name = "todo/home.html"
    success_url = reverse_lazy("main")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/list.html"
    success_url = reverse_lazy("main")
    context_object_name = "todo_list"
    form_class = TodoForm
    cards_per_page = None

    def get_queryset(self):
        self.cards_per_page = UserSettings.objects.get(
            user=self.request.user
        ).cards_per_page
        print(f"query {self.cards_per_page}")
        return Todo.objects.filter(user=self.request.user)

    def get_data(self):
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
        self.cards_per_page = self.get_data()
        set_cards_per_page(self.request.user, self.cards_per_page)
        return self.cards_per_page

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cards_per_page"] = self.cards_per_page
        return context


@method_decorator(login_required, name="dispatch")
class TodoCreateView(CreateView):
    model = Todo
    template_name = "todo/create.html"
    form_class = TodoForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
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
    model = Todo
    template_name = "todo/delete.html"
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
