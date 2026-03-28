from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import AppUserCreationForm
# from accounts.models import Profile
# from common.mixin import CheckUserIsOwner

UserModel = get_user_model()


class RegisterAppUserView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/login.html')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile_details.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# class ProfileEditView(LoginRequiredMixin, CheckUserIsOwner, UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'accounts/profile-edit-page.html'
#
#     def get_success_url(self) -> str:
#         return reverse(
#             'accounts:details',
#             kwargs={
#                 "pk": self.object.pk,
#             }
#         )
#

# def profile_delete(request: HttpRequest, pk: int) -> HttpResponse:
#     user = UserModel.object.get(pk=pk)
#
#     if request.user.is_authenticated and request.user.pk == user.pk:
#         if request.method == "POST":
#             user.delete()
#             return reverse("common:home")
#     else:
#         return HttpResponseForbidden()
#
#
#     return render(request, 'accounts/profile-delete.html')