from django.urls import path
from .views import image_page

urlpatterns = [
    path("", image_page, name="image"),
]
