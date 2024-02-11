from django.contrib import admin
from django.urls import path, include
from .models import Subscription

path('news/', include('news.urls'))

# Register your models here.
admin.site.register(Subscription)
