from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from cities.forms import CitiesForm
from cities.models import Cities
from django.contrib import messages


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
    success_message = "Градът беше създаден успешно."


class CitiesUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = 'cities.change_cities'
    model = Cities
    form_class = CitiesForm
    template_name = 'cities/cities_form.html'
    success_url = reverse_lazy('cities:cities_list')
    success_message = "Градът беше обновен успешно."



class CitiesDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = 'cities.delete_cities'
    model = Cities
    template_name = 'cities/cities_delete.html'
    success_url = reverse_lazy('cities:cities_list')

    def form_valid(self, form):
        messages.success(self.request, "Градът беше изтрит успешно.")
        return super().form_valid(form)




