from django import forms

from cities.models import Cities

class CitiesForm(forms.ModelForm):
    class Meta:
        model = Cities
        fields = ['name', 'district']


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Наименование',
            'district': 'Област',
        }

        help_texts = {
            'name': 'Въведи име на град или село без гр./с. преди него.',
            'district': 'Избери областта, в която се намира градът или селото.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Cities.objects.filter(name=name).exists():
            raise forms.ValidationError("Такъв град вече съществува.")

        return name
