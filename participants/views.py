from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from events.models import Event, Role
from .forms import UserUpdateForm, ParticipantUpdateForm, ParticipantEventRoleForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Participant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = 'participants/participant_list.html'
    context_object_name = 'participants'
    login_url = 'login'


class ParticipantDetailView(LoginRequiredMixin, DetailView):
    model = Participant
    template_name = 'participants/participant_detail.html'
    context_object_name = 'participant'
    login_url = 'login'



class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    fields = ['city', 'phone', 'car_registration_number']
    template_name = 'participants/participant_edit.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('participant_detail', kwargs={'pk': self.object.pk})


#
# class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
#     model = Participant
#     template_name = 'participants/participant_confirm_delete.html'
#     success_url = reverse_lazy('participant_list')
#     login_url = 'login'
#



def assign_role(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    roles = Role.objects.all()

    if request.method == 'POST':
        form = ParticipantEventRoleForm(request.POST, event=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event_id)
    else:
        form = ParticipantEventRoleForm(event=event)

    return render(request, 'participants/assign_role.html', {
        'form': form,
        'event': event,
        'roles': roles
    })
