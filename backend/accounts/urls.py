from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ConnexionView, InscriptionView, ProfilView

urlpatterns = [
    path("inscription/", InscriptionView.as_view(), name="inscription"),
    path("connexion/", ConnexionView.as_view(), name="connexion"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profil/", ProfilView.as_view(), name="profil"),
]
