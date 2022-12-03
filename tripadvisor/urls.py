from django.urls import path
from .views import *


urlpatterns = [
    path('tripadvisor/', tripadvisor, name = "tripadvisorScraper"),   
]
