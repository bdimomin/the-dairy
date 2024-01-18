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
    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        self.fields['case_type'].label = "Case Type"
        self.fields['mobile_no'].label = "Mobile No"
        self.fields['first_party'].label = "First Party"
        self.fields['second_party'].label = "Second Party"
        self.fields['appointed_by'].label = "Appointed By"
        self.fields['law_and_section'].label = "Law and Section"
        self.fields['case_no'].label = "Case No"
        self.fields['police_station'].label = "Police Station"
        self.fields['fixed_for'].label = "Fixed For"
        
    class Meta:
        model = Case
        exclude =['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClientForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['chamber_file_number'].label = "Chamber File Number"
        self.fields['additional_mobile'].label = "Additional Mobile"
        self.fields['short_note'].label = "Short Note"
       
    class Meta:
        model = Client
        fields = '__all__'

class BulkUploadForm(forms.ModelForm):
    class Meta:
        model = BulkUpload
        fields = ['file']