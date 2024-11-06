from django.urls import path, include
from django.views.generic import TemplateView
from . import views


app_name = "account"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/done", TemplateView.as_view(template_name="account/register_done.html"),
                          name="register_done"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
