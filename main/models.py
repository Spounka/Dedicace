import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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
class PaymentInformation(models.Model):
    ccp = models.CharField(default="0024242424/24", max_length=50, null=True)
    rip = models.CharField(default="0079999002453623936", max_length=255, null=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        if hasattr(self, 'user'):
            return f"{self.user.username} PaymentInformation"
        return f"{self.ccp}"


def profile_picture_upload_dir(instance: 'User', filename: str) -> str:
    return f'{instance.username}/images/Profile_{filename}'


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    phone_number = models.CharField(default="+213", max_length=20, unique=True)
    payment_details = models.OneToOneField(PaymentInformation, on_delete=models.SET_NULL, null=True, blank=True)

    profile_picture = models.ImageField(upload_to=profile_picture_upload_dir, null=True, blank=True)

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

    def is_client(self):
        return hasattr(self, 'client')

    def is_celebrity(self):
        return hasattr(self, 'celebrity')

    def __str__(self):
        return f"{self.phone_number}"

    @property
    def full_name(self):
        return self.get_full_name()


class Availability(models.Model):
    start_day = models.CharField(default="Sunday", max_length=10)
    end_day = models.CharField(default="Thursday", max_length=10)
    start_hour = models.CharField(default="09:00", max_length=10)
    end_hour = models.CharField(default="17:00", max_length=10)

    def __str__(self):
        return f"{self.start_day}-{self.end_day}"

    class Meta:
        verbose_name_plural = "Availabilities"


class Celebrity(models.Model):
    description = models.TextField(default="")
    price = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True, null=False, blank=False)
    user: User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    availability: Availability = models.OneToOneField(Availability, on_delete=models.SET_NULL, null=True, blank=True)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return f"Celeb - {self.user.phone_number}"

    class Meta:
        verbose_name_plural = "Celebrities"


class Client(models.Model):
    user: User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wilaya = models.CharField(max_length=35, choices=WILAYA_CHOICES, default="01")

    def __str__(self):
        return f"{self.user.username}"


def get_user_receipt_upload_folder(instance, filename):
    return f'payments/{instance.payment_date}/{filename}'


def get_date_as_long(*_, **__):
    return datetime.datetime.now().timestamp()


class Payment(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    REFUSED = 'refused'
    UPDATED = 'updated'

    STATUS_CHOICES = [
        (PENDING, _("Pending")),
        (CONFIRMED, _("Confirmed")),
        (REFUSED, _("Refused")),
        (UPDATED, _("Updated")),
    ]

    amount_paid = models.FloatField(default=0.0)
    payment_date = models.PositiveIntegerField(default=get_date_as_long)
    is_valid = models.BooleanField(default=False)
    receipt = models.ImageField(upload_to=get_user_receipt_upload_folder)
    payment_status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=10)

    def __str__(self):
        return f"Payment#{self.id}"

    @property
    def get_date_from_long(self):
        return datetime.datetime.fromtimestamp(self.payment_date)


class OfferRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', _("Pending")),
        ('accepted', _("Accepted")),
        ('refused', _("Refused")),
        ('on-going', _("On-going")),
        ('canceled', _("Canceled")),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment: Payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    sender: User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_sender")
    recepient: User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name="request_recepient")
    description = models.TextField()
    title = models.CharField(max_length=100, default="Title")

    def __str__(self):
        return f"{self.title} {self.sender.phone_number}"


def get_report_image_location(instance, filename):
    return f"reports/{instance.reporter.username}/%y-%m-%d/{filename}"


class Report(models.Model):
    reporter: User = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                       related_name="report_sender")
    reported: User = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                       related_name="report_recipient")
    report_date = models.CharField(default="", max_length=60)
    report_reason = models.TextField(default="Report Reason")
    report_image = models.ImageField(upload_to=get_report_image_location)
