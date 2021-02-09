from django.urls import path, include
from .views import frequency, result

urlpatterns = [
    path('frequency', frequency, name="frequency"),
        path('result', result, name="result"),
]
