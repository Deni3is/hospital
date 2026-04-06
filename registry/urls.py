from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import DashboardView, PatientCreateView, PatientUpdateView, UserLoginView

urlpatterns = [
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path("patients/add/", login_required(PatientCreateView.as_view()), name="patient_add"),
    path(
        "patients/<int:pk>/edit/",
        login_required(PatientUpdateView.as_view()),
        name="patient_edit",
    ),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
]
