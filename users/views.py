from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import LoginForm, ProfileForm, UserCreationForm
from .models import User


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:detail", pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


class UserLogoutView(View):
    # не использовал LogoutView, так как с django 5+ логаут только с POST запросом работает,
    # а в шаблоне там гет запрос отправляется,
    # поэтому чтобы шаблон не менять сделал view логаута для get запроса
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("users:list")


class UserListView(ListView):
    model = User
    template_name = "users/participants.html"
    context_object_name = "participants"
    ordering = ("-date_joined", "-id")
    paginate_by = 12


class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("owned_projects__participants")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.object.pk})


class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/change_password.html"

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})
