from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cities.models import Cities
from events.models import Event, Role
from .choises import DistrictChoice
from .forms import ParticipantEventRoleForm, ParticipantForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Participant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = 'participants/participant_list.html'
    context_object_name = 'participants'
    login_url = 'login'

    def get_queryset(self):
        qs = Participant.objects.select_related("city").all()

        city = self.request.GET.get("city")
        district = self.request.GET.get("district")
        sort = self.request.GET.get("sort")


        if city:
            qs = qs.filter(city_id=city)


        if district:
            qs = qs.filter(city__district=district)


        if sort == "participant.first_name_asc":
            qs = qs.order_by("first_name", "last_name")
        elif sort == "participant.first_name_desc":
            qs = qs.order_by("-first_name", "-last_name")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = Cities.objects.all().order_by("name")
        context["districts"] = DistrictChoice.choices

        return context

    def get(self, request, *args, **kwargs):
        if "clear" in request.GET:
            return redirect("participant_list")
        return super().get(request, *args, **kwargs)



class ParticipantCreateView(LoginRequiredMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participants/participant_create.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('participant_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ParticipantDetailView(LoginRequiredMixin, DetailView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participants/participant_detail.html'
    context_object_name = 'participant'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)



class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participants/participant_edit.html'
    context_object_name = "participant"
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('participant_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Participant.objects.filter(user=self.request.user)



class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
    model = Participant
    template_name = 'participants/participant_delete.html'
    success_url = reverse_lazy('participant_list')
    login_url = 'login'

    def get_queryset(self):
        return Participant.objects.filter(user=self.request.user)



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
