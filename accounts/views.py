from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib import messages

from .forms import RegisterForm
from participants.models import Participant


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(self.request, "Регистрацията е успешна! Моля, влезте в профила си.")
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Participant
    template_name = 'accounts/profile_details.html'
    context_object_name = 'participant'

    def get_object(self):
        return Participant.objects.get(user=self.request.user)
