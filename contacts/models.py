from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import User


class Contact(BaseModel):
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")

    def __str__(self):
        return self.full_name

    class Meta:
        indexes = [
            models.Index(fields=["full_name"]),
        ]


class PhoneNumber(BaseModel):
    contact = models.ForeignKey(
        Contact, related_name="phone_numbers", on_delete=models.CASCADE
    )
    number = models.CharField(max_length=13)

    def __str__(self):
        return self.number

    def normalize_phone(self, phone):
        phone = "".join(filter(str.isdigit, phone))
        if len(phone) == 12:
            return "+" + phone
        elif 10 <= len(phone) < 12:
            return "+38" + phone
        return phone

    def set_phone(self, phone):
        self.number = self.normalize_phone(phone)

    def save(self, *args, **kwargs):
        self.number = self.normalize_phone(self.number)
        super().save(*args, **kwargs)


class Tag(BaseModel):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name


class Record(BaseModel):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, default=None, null=True)
    note = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.contact.full_name}, {self.note}"
