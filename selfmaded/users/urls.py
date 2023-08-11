from django.urls import path
from .views import RegisterView, ProfileView




urlpatterns = [
    path("register/", RegisterView.as_view(), name="registration"),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile")
]