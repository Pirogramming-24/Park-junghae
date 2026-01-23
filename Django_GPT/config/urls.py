from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("/summarize/")),

    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),

    path("summarize/", include("apps.summarize.urls")),
    path("sentiment/", include("apps.sentiment.urls")),
    path("generate/", include("apps.generate.urls")),
    path("translate/", include("apps.translate.urls")),
    path("image/", include("apps.image.urls")),
]
