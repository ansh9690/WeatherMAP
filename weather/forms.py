from django.forms import TextInput, ModelForm
from .models import CityName


class CityForm(ModelForm):
    class Meta:
        model = CityName
        fields = ['city_name']
        widgets = {'city_name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}
