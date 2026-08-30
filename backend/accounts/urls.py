from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView,
    MatchCheckView,
    MatchListCreateView,
    MeView,
    SignupView,
)

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path("me", MeView.as_view(), name="me"),
    path("matches", MatchListCreateView.as_view(), name="matches"),
    path("check-match", MatchCheckView.as_view(), name="check_match"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
