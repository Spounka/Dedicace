from django.apps import apps
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

WILAYA_CHOICES = [
    ("01", _("Adrar")),
    ("02", _("Chlef")),
    ("03", _("Laghouat")),
    ("04", _("Oum El Bouaghi")),
    ("05", _("Batna")),
    ("06", _("Béjaïa")),
    ("07", _("Biskra")),
    ("08", _("Béchar")),
    ("09", _("Blida")),
    ("10", _("Bouïra")),
    ("11", _("Tamanrasset")),
    ("12", _("Tébessa")),
    ("13", _("Tlemcen")),
    ("14", _("Tiaret")),
    ("15", _("Tizi Ouzou")),
    ("16", _("Algiers")),
    ("17", _("Djelfa")),
    ("18", _("Jijel")),
    ("19", _("Sétif")),
    ("20", _("Saïda")),
    ("21", _("Skikda")),
    ("22", _("Sidi Bel Abbès")),
    ("23", _("Annaba")),
    ("24", _("Guelma")),
    ("25", _("Constantine")),
    ("26", _("Médéa")),
    ("27", _("Mostaganem")),
    ("28", _("M'Sila")),
    ("29", _("Mascara")),
    ("30", _("Ouargla")),
    ("31", _("Oran")),
    ("32", _("El Bayadh")),
    ("33", _("Illizi")),
    ("34", _("Bordj Bou Arréridj")),
    ("35", _("Boumerdès")),
    ("36", _("El Tarf")),
    ("37", _("Tindouf")),
    ("38", _("Tissemsilt")),
    ("39", _("El Oued")),
    ("40", _("Khenchela")),
    ("41", _("Souk Ahras")),
    ("42", _("Tipaza")),
    ("43", _("Mila")),
    ("44", _("Aïn Defla")),
    ("45", _("Naâma")),
    ("46", _("Aïn Témouchent")),
    ("47", _("Ghardaïa")),
    ("48", _("Relizane")),
    ("49", _("El M'Ghair")),
    ("50", _("El Menia")),
    ("51", _("Ouled Djellal")),
    ("52", _("Bordj Baji Mokhtar")),
    ("53", _("Béni Abbès")),
    ("54", _("Timimoun")),
    ("55", _("Touggourt")),
    ("56", _("Djanet")),
    ("57", _("In Salah")),
    ("58", _("Oum El Bouaghi")),
]


# noinspection DuplicatedCode
class UserManager(BaseUserManager):
    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given phone_number, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        phone_number = GlobalUserModel.normalize_username(phone_number)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)

    def with_perm(
            self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(default="+213", max_length=15, unique=True)
    ccp = models.CharField(default="0024242424/24", max_length=50)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    @classmethod
    def normalize_username(cls, username: str):
        if username.startswith("0"):
            return "".join(["+213", username[1:]])
        if username.startswith("+213"):
            if username[4] == "0":
                return username[:3] + username[5:]
            else:
                return username

    def __str__(self):
        return f"{self.phone_number}"


class Disponibility(models.Model):
    start_day = models.CharField(default="Sunday", max_length=10)
    end_day = models.CharField(default="Thursday", max_length=10)
    start_hour = models.CharField(default="09:00", max_length=10)
    end_hour = models.CharField(default="17:00", max_length=10)

    def __str__(self):
        return f"{self.start_day}-{self.end_day}"

    class Meta:
        verbose_name_plural = "Disponibilities"


class Celebrity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(default="")
    price = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True, null=False, blank=False)
    disponibility = models.OneToOneField(Disponibility, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Celeb - {self.user.username}"

    class Meta:
        verbose_name_plural = "Celebrities"


class Fan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wilaya = models.CharField(max_length=35, choices=WILAYA_CHOICES, default="01")

    def __str__(self):
        return f"{self.user.username}"


def get_user_receipt_upload_folder(instance, filename):
    return f'payments/{instance.payment_date}/{instance.id}/{filename}'


class Payment(models.Model):
    price = models.FloatField(default=0.0)
    payment_date = models.PositiveIntegerField(default=0)
    is_valid = models.BooleanField(default=False)
    receipt = models.ImageField(upload_to=get_user_receipt_upload_folder)

    def __str__(self):
        return f"Payment#{self.id}"


class Request(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    sender = models.ForeignKey(Fan, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Celebrity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender.user.username} {self.payment.payment_date}"


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                 related_name="report_sender")
    reported = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                 related_name="report_recipient")
    report_date = models.PositiveBigIntegerField(default=0)
    report_reason = models.TextField(default="Report Reason")
