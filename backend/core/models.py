from django.db import models
from django.contrib.auth.models import User
import secrets


class Token(models.Model):
    """Simple token model for API authentication"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_token')
    key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_token(cls, user):
        """Generate a new token for a user"""
        # Delete existing token if any
        cls.objects.filter(user=user).delete()
        # Generate new token
        token = cls.objects.create(
            user=user,
            key=secrets.token_urlsafe(48)
        )
        return token.key

    def __str__(self):
        return f"Token for {self.user.username}"


class Study(models.Model):
    title = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="planning")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Participant(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="participants")
    code = models.CharField(max_length=64)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=16)
    enrolled_on = models.DateField()

    def __str__(self) -> str:
        return f"{self.code} ({self.study.title})"


class LiteratureArticle(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    journal = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    doi = models.CharField(max_length=128, blank=True)
    abstract = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
