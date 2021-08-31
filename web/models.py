from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Sacco(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ending_point = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ", ending point: " + self.ending_point


class Route(models.Model):
    name = models.CharField(max_length=255, unique=True)
    saccos = models.ManyToManyField(Sacco, related_name='saccos', blank=True)
    starting_point = models.CharField(max_length=255)  # common point

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('route-detail', kwargs={'pk': self.pk})


class TLD(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="tld")

    def __str__(self):
        return str(self.number)


class BusStop(models.Model):
    tld = models.ForeignKey(TLD, on_delete=models.CASCADE)
    bus_stop = models.CharField(max_length=255)

    class Meta:
        unique_together = ['tld', 'bus_stop', ]

    def __str__(self):
        return self.bus_stop


class Fare(models.Model):
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, related_name='fare')
    distance = models.FloatField()
    fare = models.PositiveIntegerField()

    def __str__(self):
        return str(self.fare)


class Commute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commutes')
    pickup_point = models.CharField(max_length=255)
    drop_off_point = models.CharField(max_length=255)
    fare = models.ForeignKey(Fare, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user)
