from django.urls import path
from .views import sentiment_page

urlpatterns = [
    path("", sentiment_page, name="sentiment"),
]
