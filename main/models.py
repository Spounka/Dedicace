from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

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


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(default="+213", max_length=20, unique=True)
    ccp = models.CharField(default="0024242424/24", max_length=50)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    @classmethod
    def normalize_username(cls, username: str):
        if username.startswith("0"):
            return "".join(["+213", username[1:]])
        if username.startswith("+213") and len(username) > 13:
            return "".join(["+213", username[5:]])
        return username

    def __str__(self):
        return f"{self.phone_number}"


class Availability(models.Model):
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
    availability = models.OneToOneField(Availability, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Celeb - {self.user.phone_number}"

    class Meta:
        verbose_name_plural = "Celebrities"


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wilaya = models.CharField(max_length=35, choices=WILAYA_CHOICES, default="01")

    def __str__(self):
        return f"{self.user.username}"


def get_user_receipt_upload_folder(instance, filename):
    return f'payments/{instance.payment_date}/{filename}'


class Payment(models.Model):
    amount_paid = models.FloatField(default=0.0)
    payment_date = models.PositiveIntegerField(default=0)
    is_valid = models.BooleanField(default=False)
    receipt = models.ImageField(upload_to=get_user_receipt_upload_folder)

    def __str__(self):
        return f"Payment#{self.id}"


class OfferRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', _("Pending")),
        ('accepted', _("Accepted")),
        ('refused', _("Refused")),
        ('on-going', _("On-going")),
        ('canceled', _("Canceled")),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_sender")
    recepient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_recipient")

    def __str__(self):
        return f"{self.sender.username}-{self.recepient}"


def get_report_image_location(instance, filename):
    return f"/reports/{instance.reporter.user.username}/%y-%m-%d/{filename}"


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                 related_name="report_sender")
    reported = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                 related_name="report_recipient")
    report_date = models.PositiveBigIntegerField(default=0)
    report_reason = models.TextField(default="Report Reason")
    report_image = models.ImageField(upload_to=get_report_image_location)
