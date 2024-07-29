from django.urls import path

from . import views

app_name = "files"

urlpatterns = [
    path("", views.index, name="files"),
    path("files_repo/", views.files, name="files_repo"),
    path("upload/", views.upload, name="upload"),
    path("files_repo/edit/<int:f_id>", views.edit, name="edit"),
    path("files_repo/remove/<int:f_id>", views.remove, name="remove"),
]
