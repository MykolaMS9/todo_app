from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages  # flesh messages

from .forms import RegisterForm


# Create your views here.


class RegisterView(View):
    template_name = "app_auth/register.html"
    from_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="app_photo:pictures")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.from_class})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Success! Account created for {username}!")
            return redirect(to="app_auth:signin")
        return render(request, self.template_name, {"form": form})
