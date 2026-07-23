from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UtilisateurManager(BaseUserManager):
    """Gestionnaire d'utilisateurs utilisant l'email comme identifiant."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Un super-utilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Un super-utilisateur doit avoir is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class Utilisateur(AbstractUser):
    """
    Contribuable ou administrateur de la plateforme Sama Impôt.
    L'authentification se fait par email.
    """

    class TypeContribuable(models.TextChoices):
        PARTICULIER = "particulier", "Particulier"
        ENTREPRISE = "entreprise", "Entreprise / PME"
        INDEPENDANT = "independant", "Travailleur indépendant"
        COMMERCANT = "commercant", "Commerçant"

    username = None
    email = models.EmailField("adresse email", unique=True)
    telephone = models.CharField("téléphone", max_length=20, blank=True)
    adresse = models.CharField("adresse", max_length=255, blank=True)
    ninea = models.CharField(
        "NINEA / identifiant fiscal", max_length=30, blank=True,
        help_text="Numéro d'identification national des entreprises et associations.",
    )
    type_contribuable = models.CharField(
        max_length=20,
        choices=TypeContribuable.choices,
        default=TypeContribuable.PARTICULIER,
    )
    date_inscription = models.DateTimeField("date d'inscription", auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UtilisateurManager()

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        ordering = ["-date_inscription"]

    def __str__(self):
        nom_complet = f"{self.first_name} {self.last_name}".strip()
        return nom_complet or self.email

    @property
    def nom_complet(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
