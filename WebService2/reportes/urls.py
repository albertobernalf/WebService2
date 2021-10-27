from django.urls import path, include
from reportes.views import user_api_view
from django.contrib import admin

urlpatterns = [

    path('usuario/', user_api_view),
]