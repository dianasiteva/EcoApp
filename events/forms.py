from django import forms
from .models import Event, Location, Role


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event title'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'title': 'Event Title',
            'date': 'Event Date',
            'location': 'Location',
            'description': 'Description',
        }

        help_texts = {
            'title': 'Enter a short and clear event name.',
        }

        error_messages = {
            'title': {
                'required': 'Please enter a title for the event.',
            },
            'date': {
                'required': 'Please select a date.',
            },
        }



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'name': 'Location Name',
            'address': 'Address',
            'description': 'Description',
        }



class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'name': 'Role Name',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['name'].disabled = True
