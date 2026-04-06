from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class DashboardView(TemplateView):
    template_name = "registry/dashboard.html"
