import secrets

from django.db import models
from django.conf import settings


class Url(models.Model):
    url = models.URLField(max_length=255)
    hashed_url = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.pk} - {self.url} - {self.hashed_url}'

    def save(self, *args, **kwargs):
        if not self.hashed_url:
            self.hashed_url = self.hash_url()
        super().save(*args, **kwargs)

    def hash_url(self):
        token = secrets.token_urlsafe(16)[:10]
        if Url.objects.filter(hashed_url=token):
            token = self.hash_url()
        return token

    def get_full_short_url(self):
        return f'{settings.BASE_URL}{self.hashed_url}'
