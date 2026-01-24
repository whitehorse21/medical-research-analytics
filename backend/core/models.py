from django.db import models


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
