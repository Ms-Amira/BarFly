from django.contrib import admin

# Register your models here.
from .models import Bar, Beverage, Review, Photo

admin.site.register(Bar)
admin.site.register(Beverage)
admin.site.register(Review)
admin.site.register(Photo)