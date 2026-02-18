from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Location, Role
from .forms import EventForm, LocationForm


def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_delete.html', {'event': event})


def location_list(request):
    locations = Location.objects.all()
    return render(request, 'events/location_list.html', {'locations': locations})


def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'events/location_detail.html', {'location': location})


def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'events/location_form.html', {'form': form})


def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_detail', pk=pk)
    else:
        form = LocationForm(instance=location)
    return render(request, 'events/location_form.html', {'form': form})


def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('location_list')
    return render(request, 'events/location_delete.html', {'location': location})




def role_list(request):
    roles = Role.objects.all()
    return render(request, 'events/role_list.html', {'roles': roles})


def role_detail(request, pk):
    role = get_object_or_404(Role, pk=pk)
    return render(request, 'events/role_detail.html', {'role': role})