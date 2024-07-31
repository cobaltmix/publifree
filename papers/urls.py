from django.urls import path
from .views import register, submit_paper, view_papers, profile, delete_paper, contact
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", register, name="register"),
    path("submit/", submit_paper, name="submit_paper"),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("profile/", profile, name="profile"),
    path("delete-paper/<int:pk>/", delete_paper, name="delete_paper"),
    path("contact/", contact, name="contact"),
    path("", view_papers, name="view_papers"),
]
