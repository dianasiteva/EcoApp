from django.shortcuts import render, get_object_or_404, redirect

from events.models import Event, Role
from .models import Participant
from .forms import ParticipantForm, ParticipantEventRoleForm


def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'participants/participant_list.html', {'participants': participants})


def participant_detail(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    return render(request, 'participants/participant_detail.html', {'participant': participant})


def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participants/participant_form.html', {'form': form})


def participant_edit(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participants/participant_form.html', {'form': form})


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participants/participant_delete.html', {'participant': participant})




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
