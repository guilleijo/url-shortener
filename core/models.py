import hashlib
from django.db import models
from django.conf import settings


class Url(models.Model):
    url = models.URLField()
    hashed_url = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.pk} - {self.url} - {self.hashed_url}'

    def save(self, *args, **kwargs):
        if not self.hashed_url:
            self.hashed_url = self.hash_url(self.url)
        super().save(*args, **kwargs)

    def hash_url(self, url):
        return hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]

    def get_full_short_url(self):
        return f'{settings.BASE_URL}{self.hashed_url}'
