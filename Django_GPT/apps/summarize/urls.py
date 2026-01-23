from django.urls import path
from .views import summarize_page

urlpatterns = [
    path("", summarize_page, name="summarize"),
]
