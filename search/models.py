from django.db import models


class SearchDocument(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=40)
    body = models.TextField()
    embedding = models.JSONField()
    embedding_model = models.CharField(max_length=160, blank=True, default="")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
