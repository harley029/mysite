from django.forms import ModelForm, CharField, TextInput, FileInput, FileField

from files.models import File


class FileForm(ModelForm):
    description = CharField(
        max_length=300,
        min_length=5,
        widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}),
    )
    path = FileField(
        widget=FileInput(attrs={"class": "form-control", "id": "formFile"})
    )

    class Meta:
        model = File
        fields = ["description", "path"]
