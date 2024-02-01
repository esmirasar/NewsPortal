from django.contrib import admin
from django.urls import path, include

path('news/', include('news.urls'))

# Register your models here.
