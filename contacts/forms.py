from django import forms

from contacts.models import Tag, PhoneNumber, Contact, Record


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ["contact", "number"]

    def clean_number(self):
        number = self.cleaned_data.get("number")
        number = PhoneNumber().normalize_phone(number)
        # if PhoneNumber.objects.filter(number=number).exists():
        #     raise forms.ValidationError("This phone number already exists.")
        return number


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["full_name", "address", "email", "birthday"]

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if Contact.objects.filter(full_name=full_name).exists():
            raise forms.ValidationError("This author is already exists.")
        return full_name


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["contact", "note", "tags"]

    def clean(self):
        cleaned_data = super().clean()
        note = cleaned_data.get("note")
        contact = cleaned_data.get("contact")
        tags = cleaned_data.get("tags")

        if note and contact:
            # Перевірка унікальності цитати для конкретного автора
            if Record.objects.filter(note=note, contact=contact).exists():
                raise forms.ValidationError("This note for the contact already exists.")
        return cleaned_data


class SearchFormPhone(forms.Form):
    query = forms.CharField(required=True, label="Phone Number")
    def clean_number(self):
        number = self.cleaned_data.get("number")
        number = PhoneNumber().normalize_phone(number)  # нормалізуємо номер телефону
        if PhoneNumber.objects.filter(number=number).exists():
            raise forms.ValidationError("This phone number already exists.")
        return number


class SearchFormName(forms.Form):
    query = forms.CharField(label="Name", max_length=255)


class SearchFormEmail(forms.Form):
    query = forms.EmailField(required=False, label="Search by Email")


class SearchFormBirthday(forms.Form):
    query = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Search by Birthday",
    )


class SearchFormTag(forms.Form):
    query = forms.CharField(max_length=30, required=False, label="Search by Tag")


class UpdateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class UpdateContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ["full_name", "address", "email", "birthday"]

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if Contact.objects.filter(full_name=full_name).exists():
            raise forms.ValidationError("This author is already exists.")
        return full_name


class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["contact", "note", "tags"]

    def clean(self):
        cleaned_data = super().clean()
        note = cleaned_data.get("note")
        contact = cleaned_data.get("contact")
        tags = cleaned_data.get("tags")

        if note and contact:
            # Перевірка унікальності цитати для конкретного автора
            if Record.objects.filter(note=note, contact=contact).exists():
                raise forms.ValidationError("This note for the contact already exists.")
        return cleaned_data


class UpdatePhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ["contact", "number"]

    def clean_number(self):
        number = self.cleaned_data.get("number")
        number = PhoneNumber().normalize_phone(number)
        return number
