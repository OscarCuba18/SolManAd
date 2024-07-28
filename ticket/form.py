from django import forms
from .models import MaintenanceRequest, Assignament

class Maintenance_Request_Form(forms.ModelForm):
    date_required = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = MaintenanceRequest
        fields = ['date_required', 'description']

class Assignament_Form(forms.ModelForm):
    class Meta:
        model = Assignament
        fields = '__all__'
