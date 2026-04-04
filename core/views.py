from django.views.generic import TemplateView


from django.shortcuts import render

def custom_permission_denied(request, exception=None):
    return render(request, 'core/403.html', status=403)


def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)

class HomeView(TemplateView):
    template_name = 'core/home.html'





