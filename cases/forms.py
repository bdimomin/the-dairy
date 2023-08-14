# forms.py
from django import forms
from .models import Case, CaseType , Court, PoliceStation, Client, BulkUpload


class CaseTypeForm(forms.ModelForm):
    class Meta:
        model = CaseType
        fields = '__all__'

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = '__all__'

class PoliceStationForm(forms.ModelForm):
    class Meta:
        model = PoliceStation
        fields = '__all__'

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude =['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class BulkUploadForm(forms.ModelForm):
    class Meta:
        model = BulkUpload
        fields = ['file']