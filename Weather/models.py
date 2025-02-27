from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


def expiration_date():
  return  timezone.now + timedelta(minutes=10)

class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"({self.city}, {self.country})"
    
class WeatherData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    description = models.CharField(max_length=200)
    wind_speed = models.FloatField()
    
    def __str__(self):
        return f"({self.location.city}, {self.timestamp})"

class CachedWeather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=expiration_date)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"({self.location.city}, {self.timestamp})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_locations = models.ManyToManyField(Location)   
    
    def __str__(self):
        return self.user.username