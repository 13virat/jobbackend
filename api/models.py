from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Job(models.Model):

    STATUS_CHOICES = [
        ("wishlist", "Wishlist"),
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="wishlist")

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")

    salary = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    job_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    deadline = models.DateField(blank=True, null=True)
    applied_date = models.DateField(blank=True, null=True)

    interview_datetime = models.DateTimeField(blank=True, null=True)
    interview_link = models.URLField(blank=True, null=True)

    offer_date = models.DateField(blank=True, null=True)
    rejected_date = models.DateField(blank=True, null=True)

    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.position}"

    def save(self, *args, **kwargs):

        if self.status == "wishlist":
            self.applied_date = None
            self.interview_datetime = None
            self.offer_date = None
            self.rejected_date = None

        elif self.status == "applied":
            if not self.applied_date:
                self.applied_date = timezone.now().date()
            self.interview_datetime = None
            self.offer_date = None
            self.rejected_date = None

        elif self.status == "interview":
            self.offer_date = None
            self.rejected_date = None

        elif self.status == "offer":
            if not self.offer_date:
                self.offer_date = timezone.now().date()
            self.rejected_date = None

        elif self.status == "rejected":
            if not self.rejected_date:
                self.rejected_date = timezone.now().date()
            self.offer_date = None
                         
        super().save(*args, **kwargs)


class Contact(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)

    company = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    linkedin = models.URLField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Document(models.Model):

    TYPE_CHOICES = [
        ("resume", "Resume"),
        ("cover-letter", "Cover Letter"),
        ("portfolio", "Portfolio"),
        ("certificate", "Certificate"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="resume")

    file = models.FileField(upload_to="documents/", blank=True, null=True)

    url = models.URLField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title