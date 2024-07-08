from django.urls import path
from .views import download_view

urlpatterns = [
    path('download/', download_view, name='download_view'),
]
