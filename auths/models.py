from django.db import models


class Session(models.Model):
    user_id = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100)
    token = models.CharField(max_length=100, unique=True)
    access_type = models.CharField(max_length=10, default="normal")
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Session({self.token})"
