from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import DashboardView, UserLoginView

urlpatterns = [
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
]
