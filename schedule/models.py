from django.db import models


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    schedule_type = models.CharField(max_length=50)

    def __str__(self):
        return "Schedule({}, {})".format(self.date, self.schedule_type)
