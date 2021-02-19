import hashlib
from django.db import models

class Url(models.Model):
    url = models.URLField()
    short_url = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.pk} - {self.url}'

    def save(self, *args, **kwargs):
        self.short_url = self.hash_url(self.url)
        super().save(*args, **kwargs)

    def hash_url(self, url):
        return hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
