from django import forms
from .models import Participant, ParticipantEventRole


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'phone']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'email': 'Електронна поща',
            'phone': 'Телефонен номер',
        }

        error_messages = {
            'email': {
                'invalid': 'Невалиден адрес на електронна поща.',
            }
        }




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

