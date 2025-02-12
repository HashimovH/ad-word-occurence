from django.conf import settings
from django.db import models


class AudioFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    file_name = models.CharField(max_length=255, blank=True)
    search_term = models.CharField(max_length=255)
    word_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.search_term} ({self.word_count} times)"
