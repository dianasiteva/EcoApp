from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from participants.choises import DistrictChoice
from participants.models import ParticipantEventRole
from .models import Event, Location
from .forms import EventForm, LocationForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

def event_list(request):
    events = Event.objects.all()
    locations = Location.objects.all()


    location_id = request.GET.get('location')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if location_id and location_id != "":
        events = events.filter(location_id=location_id)

    if date_from:
        events = events.filter(date__gte=date_from)

    if date_to:
        events = events.filter(date__lte=date_to)


    sort = request.GET.get('sort')

    if sort == "date_asc":
        events = events.order_by('date')
    elif sort == "date_desc":
        events = events.order_by('-date')
    else:
        events = events.order_by('-date')  # default

    return render(request, 'events/event_list.html', {
        'events': events,
        'locations': locations,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    now = timezone.now().date()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'now': now,
    })



def remove_assignment(request, per_id):
    assignment = get_object_or_404(ParticipantEventRole, pk=per_id)
    event_id = assignment.event.pk
    assignment.delete()
    return redirect('event_detail', pk=event_id)


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
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_delete.html', {'event': event})

class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'events/location_list.html'
    context_object_name = 'locations'
    login_url = 'login'

    def get_queryset(self):
        qs = Location.objects.all()

        location = self.request.GET.get("location")
        district = self.request.GET.get("district")
        sort = self.request.GET.get("sort")
        search = self.request.GET.get("search")

        if location:
            qs = qs.filter(id=location)


        if district:
            qs = qs.filter(district=district)

        if search:
            qs = qs.filter(name__icontains=search)

        if sort == "name_asc":
            qs = qs.order_by("name")
        elif sort == "name_desc":
            qs = qs.order_by("-name")
        else:
            qs = qs.order_by("name")

        return qs

    def get(self, request, *args, **kwargs):
        if "clear" in request.GET:
            return redirect("location_list")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["all_locations"] = Location.objects.all().order_by("name")
        context["districts"] = DistrictChoice.choices

        return context





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
            return redirect('location_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'events/location_form.html', {'form': form})


def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('location_list')
    return render(request, 'events/location_delete.html', {'location': location})



