from django.conf import settings

def contact_email(request):
    return {
        "EMAIL_HOST_USER": getattr(settings, "EMAIL_HOST_USER", None)
    }
