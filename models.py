from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class AdminDetails(models.Model):
    admin_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # stored as hashed value
    last_login = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        """Hashes and stores password safely."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Returns True if password matches the stored hash."""
        return check_password(raw_password, self.password)

    def update_last_login(self):
        """Updates last login time."""
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def __str__(self):
        return self.admin_name
