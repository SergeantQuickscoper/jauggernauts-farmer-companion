from django.db import models
from django.contrib.auth.models import User

class CropActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crop_activities')
    sowing_date = models.DateField(null=True, blank=True)
    last_irrigation_date = models.DateField(null=True, blank=True)
    last_fertilizer_date = models.DateField(null=True, blank=True)
    last_fertilizer_type = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    area = models.FloatField(null=True, blank=True)  # in acres or hectares
    district = models.CharField(max_length=100, null=True, blank=True)
    crops = ArrayField(
        models.CharField(max_length=50, blank=True),
        default=list,  # Important for mutability
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s crop activity ({self.sowing_date})"