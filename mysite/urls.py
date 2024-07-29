from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("", include("contacts.urls")),
    path("users/", include("users.urls")),
    path("rss/", include("rss.urls")),
    path("files/", include("files.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
