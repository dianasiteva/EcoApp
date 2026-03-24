from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


# def home(request):
#     return render(request, 'core/home.html')


def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)

class HomeView(TemplateView):
    template_name = 'core/home.html'


