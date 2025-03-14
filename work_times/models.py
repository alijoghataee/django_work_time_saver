from django.db import models

from accounts.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    hex_color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class WorkTime(models.Model):
    user = models.ForeignKey(User, related_name='work_times', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='work_times', on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    worked_minutes = models.IntegerField(blank=True, null=True)

    def save(self):
        if self.end_time:
            self.worked_minutes = (self.end_time - self.start_time).total_seconds() / 60
        super().save()
