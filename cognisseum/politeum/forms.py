from django import forms
from .models import Country, FirstLevelDivision, SecondLevelDivision, Person, Biography

class NewCountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('name', 'ip_created', 'ip_last_updated', 'user_created', 'user_last_updated')