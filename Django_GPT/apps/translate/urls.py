from django.urls import path
from .views import translate_page

urlpatterns = [
    path("", translate_page, name="translate"),
]
