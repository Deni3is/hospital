from django import forms
from django.utils import timezone

from .models import Device, Patient


class DateInput(forms.DateInput):
    input_type = "date"


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["gender", "birth_date"]
        labels = {
            "gender": "Пол",
            "birth_date": "Дата рождения",
        }
        widgets = {
            "birth_date": DateInput(),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        if birth_date > timezone.localdate():
            raise forms.ValidationError("Дата рождения не может быть в будущем.")
        return birth_date


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ["uid1", "uid2", "uid3", "brand", "model", "name"]
        labels = {
            "uid1": "UID1",
            "uid2": "UID2",
            "uid3": "UID3",
            "brand": "Бренд",
            "model": "Модель",
            "name": "Название",
        }
        error_messages = {
            "uid1": {"required": "Обязательное поле."},
            "uid2": {"required": "Обязательное поле."},
            "uid3": {"required": "Обязательное поле."},
            "brand": {"required": "Обязательное поле."},
            "model": {"required": "Обязательное поле."},
            "name": {"required": "Обязательное поле."},
        }

    def clean(self):
        cleaned_data = super().clean()
        for field_name in ["uid1", "uid2", "uid3", "model", "name"]:
            value = cleaned_data.get(field_name)
            if value is not None:
                cleaned_data[field_name] = value.strip()
        return cleaned_data
