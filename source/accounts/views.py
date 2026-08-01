from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm

User = get_user_model()


class RegisterView(CreateView):
    form_class = MyUserCreationForm
    template_name = "accounts/registration.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        redirect_url = reverse("albumApp:photos")

        if self.request.GET.get("next"):
            redirect_url = self.request.GET.get("next")

        if self.request.POST.get("next"):
            redirect_url = self.request.POST.get("next")
        return redirect_url


class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_owner = self.object
        if self.request.user.is_authenticated and self.request.user.pk == profile_owner.pk:
            context['albums'] = profile_owner.albums.order_by('-created_at')
            context['photos'] = profile_owner.photos.filter(album__isnull=True).order_by('-created_at')
            context['is_my'] = True
        else:
            context['albums'] = profile_owner.albums.filter(is_public=True).order_by('-created_at')
            context['photos'] = profile_owner.photos.filter(album__isnull=True, is_public=True).order_by('-created_at')
            context['is_my'] = False
        return context

class UserChangeView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'accounts/user_change.html'
    context_object_name = 'user_obj'

    def has_permission(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()

        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response
    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}

        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/user_password_change.html'

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.request.user.pk})
