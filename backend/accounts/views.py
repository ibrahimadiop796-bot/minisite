from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ConnexionTokenSerializer,
    InscriptionSerializer,
    UtilisateurSerializer,
)

Utilisateur = get_user_model()


class InscriptionView(generics.CreateAPIView):
    """Inscription d'un nouveau contribuable."""

    queryset = Utilisateur.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Compte créé avec succès.",
                "utilisateur": UtilisateurSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ConnexionView(TokenObtainPairView):
    """Connexion : renvoie les tokens JWT et le profil."""

    serializer_class = ConnexionTokenSerializer
    permission_classes = [permissions.AllowAny]


class ProfilView(generics.RetrieveUpdateAPIView):
    """Consultation et mise à jour du profil connecté."""

    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
