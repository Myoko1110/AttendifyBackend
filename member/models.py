from django.db import models


class Member(models.Model):
    last_name = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100, default="")
    part = models.CharField(max_length=100, default="")
    grade = models.CharField(max_length=30, default="")
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
