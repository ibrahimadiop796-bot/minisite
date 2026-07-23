from rest_framework import serializers

from .models import CategorieImpot, Impot, Notification


class CategorieImpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieImpot
        fields = ["id", "nom", "description"]


class ImpotSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source="categorie.nom", read_only=True)
    statut_courant = serializers.SerializerMethodField()
    statut_libelle = serializers.SerializerMethodField()
    contribuable = serializers.CharField(source="utilisateur.nom_complet", read_only=True)

    class Meta:
        model = Impot
        fields = [
            "id", "reference", "libelle", "categorie", "categorie_nom",
            "montant", "annee_fiscale", "date_echeance", "statut",
            "statut_courant", "statut_libelle", "contribuable", "date_creation",
        ]
        read_only_fields = ["reference", "statut", "date_creation"]

    def get_statut_courant(self, obj):
        return obj.statut_courant()

    def get_statut_libelle(self, obj):
        return Impot.Statut(obj.statut_courant()).label


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "titre", "message", "type", "lu", "date_creation"]
        read_only_fields = ["date_creation"]
