
from django.urls import path

from .views import PanchayathListView, WardListView

urlpatterns = [
    path("panchayaths/", PanchayathListView.as_view(), name="panchayath-list"),
    path("wards/", WardListView.as_view(), name="ward-list"),
]
