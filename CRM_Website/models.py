from django.db import models

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")