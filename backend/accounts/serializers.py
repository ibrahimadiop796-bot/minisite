from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

Utilisateur = get_user_model()


class UtilisateurSerializer(serializers.ModelSerializer):
    nom_complet = serializers.CharField(read_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            "id", "email", "first_name", "last_name", "nom_complet",
            "telephone", "adresse", "ninea", "type_contribuable",
            "is_staff", "date_inscription",
        ]
        read_only_fields = ["id", "is_staff", "date_inscription"]


class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            "email", "first_name", "last_name", "telephone",
            "adresse", "ninea", "type_contribuable", "password", "password2",
        ]

    def validate_email(self, value):
        if Utilisateur.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Un compte existe déjà avec cet email.")
        return value.lower()

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError(
                {"password2": "Les deux mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        return Utilisateur.objects.create_user(password=password, **validated_data)


class ConnexionTokenSerializer(TokenObtainPairSerializer):
    """Ajoute les informations de l'utilisateur au token de connexion."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["utilisateur"] = UtilisateurSerializer(self.user).data
        return data
