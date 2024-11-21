from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('authorization/', views.authorization_api_view),
    path('login/', views.LoginView.as_view()),
    path('confirm_sms/', views.ConfirmSmsView.as_view())
]