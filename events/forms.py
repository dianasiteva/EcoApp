from django import forms
from .models import Event, Location, Role


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'description']


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименование'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # 'date': forms.DateInput(format='%d.%m.%Y',attrs={'class': 'form-control','placeholder': 'дд.мм.гггг'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'title': 'Наименование на събитието',
            'date': 'Дата на събитието',
            'location': 'Локация',
            'description': 'Разяснения',
        }

        help_texts = {
            'title': 'Въведи кратко и дотатъчно описващо наименование.',
        }

        error_messages = {
            'title': {
                'required': 'Моля въведете име на събитието.',
            },
            'date': {
                'required': 'Моля посочете дата.',
            },
        }



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'description', 'district', 'latitude', 'longitude']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

        labels = {
            'name': 'Наименование',
            'address': 'Адрес',
            'description': 'Описание',
            'district': 'Област',
            'latitude': 'Географска ширина',
            'longitude': 'Географска дължина',
        }
