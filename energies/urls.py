from django.urls import path, include

from .views import ListAPIView

urlpatterns = [
    path('', ListAPIView.as_view(), name="list")
]
