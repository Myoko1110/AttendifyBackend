from django.db import models


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    date = models.DateField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id


class Response(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.CharField(max_length=50)
    date = models.DateField()
    grade = models.CharField(max_length=50, default="")
