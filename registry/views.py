from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import PatientForm
from .models import Device, Patient


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class DashboardView(TemplateView):
    template_name = "registry/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_tab = self.request.GET.get("tab", "patients")
        if active_tab not in {"patients", "devices"}:
            active_tab = "patients"

        context.update(
            active_tab=active_tab,
            patients=Patient.objects.order_by("id"),
            devices=Device.objects.order_by("id"),
        )
        return context


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "registry/patient_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            form_title="Добавить пациента",
            form_submit_label="Сохранить",
            cancel_url=reverse("dashboard") + "?tab=patients",
        )
        return context

    def get_success_url(self):
        return reverse("dashboard") + "?tab=patients"


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "registry/patient_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            form_title="Изменить пациента",
            form_submit_label="Обновить",
            cancel_url=reverse("dashboard") + "?tab=patients",
        )
        return context

    def get_success_url(self):
        return reverse("dashboard") + "?tab=patients"
