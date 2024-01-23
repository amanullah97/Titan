from django import forms
from django.forms import ModelForm
from .models import Patient # Import your Patient model
from django.contrib.auth.models import User


class PatientForm(ModelForm):
    # assistant = forms.ModelChoiceField(queryset=TitanUser.objects.all())
    class Meta:
        model = Patient
        fields = "__all__"
        exclude = ["operator"]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'registration_date': forms.DateInput(attrs={'type': 'date'}),
            'patient_appointment': forms.DateInput(attrs={'type': 'date'}),
            'last_appointment': forms.DateInput(attrs={'type': 'date'}),
            'follow_up': forms.DateInput(attrs={'type': 'date'}),
            'last_anthropometric_date': forms.DateInput(attrs={'type': 'date'}),
            'reading_date': forms.DateInput(attrs={'type': 'date'}),
            'bw_done': forms.DateInput(attrs={'type': 'date'}),
            'hb1ac_date': forms.DateInput(attrs={'type': 'date'}),
            'fobt_date': forms.DateInput(attrs={'type': 'date'}),
            'colonoscopy_date': forms.DateInput(attrs={'type': 'date'}),
            'pap_smear_date': forms.DateInput(attrs={'type': 'date'}),
            'mammogram_date': forms.DateInput(attrs={'type': 'date', 'label' : '(Female Patients Only)'}),
            'last_uds_date': forms.DateInput(attrs={'type': 'date'}),
            'last_hospital_vist': forms.DateInput(attrs={'type': 'date'}),
            'annual_wellness_vist': forms.DateInput(attrs={'type': 'date'}),
            'acp': forms.DateInput(attrs={'type': 'date'}),
            'med_reconcile_date': forms.DateInput(attrs={'type': 'date'}),
            'cologuard_date': forms.DateInput(attrs={'type': 'date'}),
        }
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['assistant'].label_from_instance = lambda obj: obj.first_name
    #     self.fields['assistant'].to_field_name = 'username'  # Use the appropriate field here
