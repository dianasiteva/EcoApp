from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from cities.forms import CitiesForm
from cities.models import Cities


class CitiesListView(LoginRequiredMixin, ListView):
    model = Cities
    template_name = 'cities/cities_list.html'
    context_object_name = 'cities'

    def get_queryset(self):
        return Cities.objects.order_by('name')



class CitiesCreateView(LoginRequiredMixin, CreateView):
    model = Cities
    form_class = CitiesForm
    template_name = 'cities/cities_form.html'
    success_url = reverse_lazy('cities:cities_list')


class CitiesUpdateView(LoginRequiredMixin, UpdateView):
    model = Cities
    form_class = CitiesForm
    template_name = 'cities/cities_form.html'
    success_url = reverse_lazy('cities:cities_list')


class CitiesDeleteView(LoginRequiredMixin, DeleteView):
    model = Cities
    template_name = 'cities/cities_delete.html'
    success_url = reverse_lazy('cities:cities_list')



