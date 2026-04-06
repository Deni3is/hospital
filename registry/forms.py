from django import forms
from django.utils import timezone

from .models import Patient


class DateInput(forms.DateInput):
    input_type = "date"


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["gender", "birth_date"]
        widgets = {
            "birth_date": DateInput(),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        if birth_date > timezone.localdate():
            raise forms.ValidationError("Дата рождения не может быть в будущем.")
        return birth_date
