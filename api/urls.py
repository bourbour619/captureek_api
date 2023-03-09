from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('users/login/', views.LoginView.as_view(), name='token'),
    path('users/verify/', views.VerifyView.as_view(), name='verify'),
    path('users/register/', views.RegisterView.as_view(), name='register'),
    path('records/', views.RecordList.as_view()),
    path('records/<int:pk>/', views.RecordDetail.as_view())
]

