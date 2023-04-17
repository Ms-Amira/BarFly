from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from datetime import date


class Beverage(models.Model):
    bev_name = models.CharField(max_length=50)
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=25, decimal_places=2, validators=[MinValueValidator(1)])
    is_alcohol = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bev_name}"


BOOLS = (
    (True , 'Yes'),
    (False, 'No')
)


class Bar(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    theme = models.CharField(max_length=50)
    site_traffic = models.IntegerField()
    has_cover = models.BooleanField(default=BOOLS[0][0], choices=BOOLS)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    beverages = models.ManyToManyField(Beverage)

    def __str__(self):
        return f"{self.name}"


class Photo(models.Model):
    url = models.CharField(max_length=200)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    beverages = models.ForeignKey(Beverage, on_delete=models.CASCADE)




RATING = (
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
)


class Review(models.Model):
    date = models.DateField()
    rating = models.IntegerField(choices=RATING, default=RATING[0][0])
    comment = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)