from django.urls import path
from account.api.views import (
    registration_view,
    ObtainAuthTokenView
)

app_name = "account"

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', ObtainAuthTokenView.as_view(), name='login'),
]
