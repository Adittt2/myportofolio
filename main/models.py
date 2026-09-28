import uuid
from django.db import models
from django.conf import settings

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

    starred_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="starred_experiences",
        blank=True,
    )

class Certification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issued_date = models.DateField()
    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.issuer}"