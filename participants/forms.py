from django import forms

from cities.models import Cities
from .models import Participant, ParticipantEventRole


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'contact_email', 'phone', 'city', 'car_registration_number', 'profile_picture']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            # 'district': forms.EmailInput(attrs={'class': 'form-control'}),
            'car_registration_number': forms.TextInput(attrs={'class': 'form-control'}),

        }

        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'contact_email': 'Електронна поща',
            'phone': 'Телефонен номер',
            'city': 'Град',
            # 'district': 'Област',
            'car_registration_number': 'Регистрационен номер на автомобил (по избор)',
            'profile_picture': 'Профилна снимка/аватар'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = Cities.objects.all().order_by('name')



class ParticipantUpdateForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'contact_email', 'city', 'car_registration_number', 'phone']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'car_registration_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'first_name': '',
            'last_name': '',
            'contact_email': '',
            'phone': 'Телефонен номер',
            'city': 'Град',
            'car_registration_number': 'Регистрационен номер на автомобил (по избор)',
        }

        error_messages = {
            'car_registration_number': {
                'invalid': 'Невалиден регистрационен номер на автомобил.',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = Cities.objects.all().order_by('name')



class ParticipantEventRoleForm(forms.ModelForm):
    class Meta:
        model = ParticipantEventRole
        fields = ['participant', 'role', 'information']

        labels = {
                     'participant': 'Доброволец',
                     'role': 'Роля',
        'information': 'Допълнителна информация',}


    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.event = self.event
        if commit:
            instance.save()
        return instance


