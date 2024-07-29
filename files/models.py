from pathlib import Path
from uuid import uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_file_size(value):
    filesize = value.size
    max_filesize = 100_000_000  # 100 MB

    if filesize > max_filesize:
        raise ValidationError(f"The file size is {filesize} bytes, which exceeds the maximum allowed size of {max_filesize} bytes.")
    return value

def validate_file_type(value):
    allowed_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "application/pdf",
        "application/msword",  # .doc
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
        "application/vnd.ms-excel",  # .xls
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
        "application/vnd.ms-powerpoint",  # .ppt
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
    ]
    file_type = value.file.content_type

    if file_type not in allowed_types:
        raise ValidationError(f"The file type {file_type} is not supported. Allowed types are: {', '.join(allowed_types)}.")
    return value


def upload_file(instance, filename):
    upload_to = (
        Path(instance.user.username) if instance.user else Path("files_repository")
    )
    ext = Path(filename).suffix
    new_filename = f"{uuid4().hex}{ext}"
    return str(upload_to / new_filename)


class File(models.Model):
    description = models.CharField(max_length=300)
    path = models.FileField(upload_to=upload_file, validators=[validate_file_size])
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
