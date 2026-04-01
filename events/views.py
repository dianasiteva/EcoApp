from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from participants.choises import DistrictChoice
from participants.models import ParticipantEventRole
from .models import Event, Location
from .forms import EventForm, LocationForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = ['-date']

    def get_queryset(self):
        qs = super().get_queryset()

        location_id = self.request.GET.get('location')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        sort = self.request.GET.get('sort')

        if location_id:
            qs = qs.filter(location_id=location_id)

        if date_from:
            qs = qs.filter(date__gte=date_from)

        if date_to:
            qs = qs.filter(date__lte=date_to)

        if sort == "date_asc":
            qs = qs.order_by('date')
        elif sort == "date_desc":
            qs = qs.order_by('-date')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now().date()
        return context


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'events.add_event'
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')
    success_message = "Събитието беше създадено успешно."


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'events.change_event'
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')
    success_message = "Събитието беше обновено успешно."


class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'events.delete_event'
    model = Event
    template_name = 'events/event_delete.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        messages.success(self.request, "Събитието беше изтрито успешно.")
        return super().form_valid(form)

class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'events/location_list.html'
    context_object_name = 'locations'
    login_url = 'accounts:login'

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


class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    template_name = 'events/location_detail.html'
    context_object_name = 'location'


class LocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'events.add_location'
    model = Location
    form_class = LocationForm
    template_name = 'events/location_form.html'
    success_url = reverse_lazy('location_list')
    success_message = "Локацията беше създадена успешно."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'events.change_location'
    model = Location
    form_class = LocationForm
    template_name = 'events/location_form.html'
    success_url = reverse_lazy('location_list')
    success_message = "Локацията беше обновена успешно."

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            messages.error(self.request, "Нямате право да редактирате тази локация.")
            return redirect('location_list')
        return obj


class LocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'events.delete_location'
    model = Location
    template_name = 'events/location_delete.html'
    success_url = reverse_lazy('location_list')

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            messages.error(self.request, "Нямате право да изтриете тази локация.")
            return redirect('location_list')
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Локацията беше изтрита успешно.")
        return super().form_valid(form)


class RemoveAssignmentView(LoginRequiredMixin, View):

    def post(self, request, per_id):
        assignment = get_object_or_404(ParticipantEventRole, pk=per_id)

        # if assignment.participant.user != request.user:
        #     messages.error(request, "Нямате право да премахвате този доброволец.")
        #     return redirect('event_detail', pk=assignment.event.pk)

        assignment.delete()
        messages.success(request, "Доброволецът беше премахнат успешно.")
        return redirect('event_detail', pk=assignment.event.pk)
