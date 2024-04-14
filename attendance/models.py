from django.db import models


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    date = models.DateField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id
