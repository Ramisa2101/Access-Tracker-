from django.db import models
from visitors.models import UserDetails
from django.utils import timezone

class HostList(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    no_of_hosts = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.name} ({self.designation})"


class AccessDetails(models.Model):
    visitor = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    host = models.ForeignKey(HostList, on_delete=models.SET_NULL, null=True)
    purpose = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    time_of_access = models.TimeField(default=timezone.now)
    no_of_visitors_today = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.visitor.name} - {self.date} ({self.host})"
