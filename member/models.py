from django.db import models


class Member(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    last_name = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100, default="")
    part = models.CharField(max_length=100, default="")
    grade = models.CharField(max_length=30, default="")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
