from django.contrib import admin

from contacts.models import Contact, PhoneNumber, Tag, Record
from rss.models import News
from files.models import File


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "birthday", "address", "author")
    list_filter = ("full_name", "email", "birthday",)
    search_fields = ("full_name", "email", "birthday")


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("contact", "note")
    list_filter = ("contact", "note")
    search_fields = ("contact__full_name", "note")


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("contact", "number")
    list_filter = ("contact", "number")
    search_fields = ("contact__full_name", "number")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(File)
class FilesAdmin(admin.ModelAdmin):
    list_display = ("user", "description", "path")
    search_fields = ("title",)


# admin.site.register(Contact)
# admin.site.register(Record)
# admin.site.register(PhoneNumber)
# admin.site.register(Tag)
