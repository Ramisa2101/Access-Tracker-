from django.db import models

class UserDetails(models.Model):
    contact_no = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    company_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nid_passport = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='visitor_photos/', blank=True, null=True)  # taken later

    def __str__(self):
        return f"{self.name} ({self.contact_no})"

class UserDetailsRecord(models.Model):
    """
    Historical snapshot of a UserDetails row before it was edited.
    """
    original_contact_no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    company_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nid_passport = models.CharField(max_length=50, blank=True, null=True)
    image_path = models.CharField(max_length=500, blank=True, null=True)  # store previous image path or name

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record of {self.original_contact_no} at {self.changed_at.isoformat()}"