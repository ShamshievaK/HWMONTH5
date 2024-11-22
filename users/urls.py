from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.RegisterAPIView.as_view()),
    path('authorization/', views.AuthAPIView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('confirm_sms/', views.ConfirmSmsView.as_view())
]