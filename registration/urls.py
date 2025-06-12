from .views import LoginView, LogoutView, RegisterView
from django.urls import path

urlpatterns = [
    path('singup/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
