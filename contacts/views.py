from django.views.generic import (
    ListView,
    DetailView,
    View,
    TemplateView,
    FormView,
    DeleteView,
)
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta

from contacts.models import Record, Contact, PhoneNumber, Tag
from contacts.forms import (
    TagForm,
    PhoneNumberForm,
    ContactForm,
    RecordForm,
    SearchFormName,
    SearchFormPhone,
    SearchFormEmail,
    SearchFormBirthday,
    SearchFormTag,
    UpdateTagForm,
    UpdateContactForm,
    UpdateRecordForm,
    UpdatePhoneNumberForm,
)

import logging
logger = logging.getLogger(__name__)
from django import forms

@method_decorator(login_required, name="dispatch")
class MainView(ListView):
    model = Record
    template_name = "contacts/index.html"
    context_object_name = "records"
    # paginate_by = 5

    def get_queryset(self):
        return Record.objects.filter(contact__author=self.request.user).order_by("contact__full_name")


@method_decorator(login_required, name="dispatch")
class RecordDetailView(DetailView):
    model = Contact
    template_name = "contacts/contact_details.html"
    context_object_name = "contact"
    pk_url_kwarg = "contact_id"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["phone_numbers"] = PhoneNumber.objects.filter(contact=self.object)
        # Отримуємо першу нотатку або None, якщо записів немає
        record = Record.objects.filter(contact=self.object).first()
        context["note"] = record.note if record else "No notes available"
        return context


@method_decorator(login_required, name="dispatch")
class TagDetailView(View):
    def get(self, request, tag_name, page=1):
        records = Record.objects.filter(tags__name=tag_name).order_by('contact__full_name')
        paginator = Paginator(records, 10)
        page_number = request.GET.get("page", page)
        records_on_page = paginator.get_page(page_number)
        return render(
            request,
            "contacts/tag_details.html",
            context={"tag": tag_name, "contacts": records_on_page},
        )


@method_decorator(login_required, name="dispatch")
class AddBookView(TemplateView):
    template_name = "contacts/add/add_book.html"


@method_decorator(login_required, name="dispatch")
class AddTagView(TemplateView):
    template_name = "contacts/add/add_tag.html"

    def get(self, request):
        form = TagForm()
        return self.render_to_response({"form": form})

    def post(self, request):
        if "cancel" in request.POST:
            return redirect("add_book")
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_tag")
        return self.render_to_response({"form": form})


@method_decorator(login_required, name="dispatch")
class AddPhoneView(TemplateView):
    template_name = "contacts/add/add_phone.html"

    def get(self, request, *args, **kwargs):
        form = (PhoneNumberForm())
        return self.render_to_response({"form": form})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("add_book")
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_phone")
        return self.render_to_response({"form": form})


@method_decorator(login_required, name="dispatch")
class AddContactView(TemplateView):
    template_name = "contacts/add/add_contact.html"

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return self.render_to_response({"form": form})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("add_book")
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.author = (request.user)
            contact.save()
            return redirect("add_contact")
        return self.render_to_response({"form": form})


@method_decorator(login_required, name="dispatch")
class AddRecordView(TemplateView):
    template_name = "contacts/add/add_record.html"

    def get(self, request, *args, **kwargs):
        form = RecordForm()
        return self.render_to_response({"form": form})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("add_book")
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.author = request.user
            record.save()
            form.save_m2m()  # Зберегти зв'язок Many-to-Many
            return redirect("add_record")
        return self.render_to_response({"form": form})


@method_decorator(login_required, name="dispatch")
class DeleteView(TemplateView):
    template_name = "contacts/delete/delete_main.html"


@method_decorator(login_required, name="dispatch")
class PhoneDeleteListView(View):
    def get(self, request):
        phone_numbers = PhoneNumber.objects.all()
        return render(request, "contacts/delete/delete_phone_list.html", {"phone_numbers": phone_numbers})


@method_decorator(login_required, name="dispatch")
class PhoneDeleteConfirmView(View):
    def get(self, request, pk):
        phone_number = get_object_or_404(PhoneNumber, pk=pk)
        return render(request, "contacts/delete/confirm_delete_phone.html", {"object": phone_number})

    def post(self, request, pk):
        phone_number = get_object_or_404(PhoneNumber, pk=pk)
        phone_number.delete()
        return redirect("phone_number_delete_list")


@method_decorator(login_required, name="dispatch")
class TagDeleteListView(View):
    def get(self, request):
        tags = Tag.objects.all()
        return render(request, "contacts/delete/delete_tag_list.html", {"tags": tags})


@method_decorator(login_required, name="dispatch")
class TagDeleteConfirmView(View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        return render(request, "contacts/delete/confirm_delete_tag.html", {"object": tag})

    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return redirect("tag_delete_list")


@method_decorator(login_required, name="dispatch")
class NoteDeleteListView(View):
    def get(self, request):
        notes = Record.objects.filter(note__isnull=False).distinct()  # Отримати всі записи з нотатками
        return render(request, "contacts/delete/delete_note_list.html", {"notes": notes})


@method_decorator(login_required, name="dispatch")
class NoteDeleteConfirmView(View):
    def get(self, request, pk):
        note_record = get_object_or_404(Record, pk=pk)
        return render(request, "contacts/delete/confirm_delete_note.html", {"object": note_record})

    def post(self, request, pk):
        note_record = get_object_or_404(Record, pk=pk)
        note_record.note = None  # Видалити нотатку
        note_record.save()
        return redirect("note_delete_list")


@method_decorator(login_required, name="dispatch")
class ContactDeleteListView(View):
    def get(self, request):
        contacts = Contact.objects.filter(author=request.user)
        return render(request, "contacts/delete/delete_contact_list.html", {"contacts": contacts})


@method_decorator(login_required, name="dispatch")
class ContactDeleteConfirmView(View):
    def get(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk, author=request.user)
        return render(request, "contacts/delete/confirm_delete_contact.html", {"object": contact})

    def post(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk, author=request.user)
        contact.delete()
        return redirect("contact_delete_list")


@method_decorator(login_required, name="dispatch")
class SearchView(TemplateView):
    template_name = "contacts/search/search_main.html"


@method_decorator(login_required, name="dispatch")
class SearchViewName(FormView):
    template_name = "contacts/search/search_results.html"
    form_class = SearchFormName

    def get(self, request):
        if "query" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=self.form_class())
            )

    def form_valid(self, form):
        query = form.cleaned_data.get("query")
        results = Contact.objects.filter(
            full_name__icontains=query, author=self.request.user
        )
        return self.render_to_response(
            self.get_context_data(results=results, form=form)
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name="dispatch")
class SearchViewPhone(FormView):
    template_name = "contacts/search/search_results.html"
    form_class = SearchFormPhone

    def get(self, request):
        if "query" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=self.form_class())
            )

    def form_valid(self, form):
        query = form.cleaned_data.get("query")
        # Фільтруємо по телефонним номерам
        phone_numbers = PhoneNumber.objects.filter(number__icontains=query)
        # Отримуємо унікальні контакти
        contact_ids = phone_numbers.values_list("contact_id", flat=True)
        results = Contact.objects.filter(id__in=contact_ids, author=self.request.user)
        return self.render_to_response(self.get_context_data(results=results, form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name="dispatch")
class SearchViewEmail(FormView):
    template_name = "contacts/search/search_results.html"
    form_class = SearchFormEmail

    def get(self, request):
        if "query" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=self.form_class())
            )

    def form_valid(self, form):
        query = form.cleaned_data.get("query")
        results = Contact.objects.filter(
            email__icontains=query, author=self.request.user
        )
        return self.render_to_response(
            self.get_context_data(results=results, form=form)
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name="dispatch")
class SearchViewBirthday(FormView):
    template_name = "contacts/search/search_results.html"
    form_class = SearchFormBirthday

    def get(self, request, *args, **kwargs):
        if "query" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=self.form_class())
            )

    def form_valid(self, form):
        query = form.cleaned_data.get("query")
        # Assuming `query` is in 'YYYY-MM-DD' format
        results = Contact.objects.filter(birthday=query, author=self.request.user)
        return self.render_to_response(
            self.get_context_data(results=results, form=form)
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name="dispatch")
class SearchViewTag(FormView):
    template_name = "contacts/search/search_results.html"
    form_class = SearchFormTag

    def get(self, request, *args, **kwargs):
        if "query" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.render_to_response(self.get_context_data(form=self.form_class()))

    def form_valid(self, form):
        query = form.cleaned_data.get("query")
        # Фільтруємо записи за тегами
        tags = Tag.objects.filter(name__icontains=query)
        contact_ids = Record.objects.filter(tags__in=tags).values_list("contact_id", flat=True)
        results = Contact.objects.filter(id__in=contact_ids, author=self.request.user)
        return self.render_to_response(self.get_context_data(results=results, form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



@method_decorator(login_required, name="dispatch")
class SearchViewUpcomingBirthdays(ListView):
    template_name = "contacts/search/search_results.html"
    context_object_name = "results"

    def get_queryset(self):
        today = timezone.now().date()
        next_week = today + timedelta(days=7)
        current_month_birthdays = Contact.objects.filter(
            birthday__month=today.month,
            birthday__day__range=(today.day, 31),
            author=self.request.user,
        )
        next_month_birthdays = Contact.objects.filter(
            birthday__month=next_week.month,
            birthday__day__range=(1, next_week.day),
            author=self.request.user,
        )
        results = current_month_birthdays | next_month_birthdays
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = None  # Форма не потрібна
        return context


@method_decorator(login_required, name="dispatch")
class UpdateView(TemplateView):
    template_name = "contacts/update/update_main.html"


@method_decorator(login_required, name="dispatch")
class TagListView(ListView):
    model = Tag
    template_name = "contacts/update/tag_list.html"
    context_object_name = "tags"


@login_required
def update_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = UpdateTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect("tag_list")
    else:
        form = UpdateTagForm(instance=tag)
    return render(
        request, "contacts/update/update_tag.html", {"form": form, "tag": tag}
    )


@method_decorator(login_required, name="dispatch")
class ContactListView(ListView):
    model = Contact
    template_name = "contacts/update/contact_list.html"
    context_object_name = "contacts"

    def get_queryset(self):
        return (
            Contact.objects.filter(author=self.request.user)
            .select_related("author")
            .order_by("full_name")
        )


@login_required
def update_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = UpdateContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect("contact_list")
    else:
        form = UpdateContactForm(instance=contact)
    return render(request, "contacts/update/update_contact.html", {"form": form, "contact": contact})


@method_decorator(login_required, name="dispatch")
class RecordListView(ListView):
    model = Record
    template_name = "contacts/update/note_list.html"
    context_object_name = "notes"

    def get_queryset(self):
        # Отримати всі нотатки, у яких є значення (не пусті)
        return Record.objects.filter(note__isnull=False).distinct()


@login_required
def update_note(request, pk):
    note = get_object_or_404(Record, pk=pk)
    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = UpdateRecordForm(instance=note)
    return render(
        request,
        "contacts/update/update_note.html",
        {"form": form, "note": note}
    )


@method_decorator(login_required, name="dispatch")
class PhoneNumberListView(ListView):
    model = PhoneNumber
    template_name = "contacts/update/phone_number_list.html"
    context_object_name = "phone_numbers"


@login_required
def update_phone_number(request, pk):
    phone_number = get_object_or_404(PhoneNumber, pk=pk)

    if request.method == "POST":
        form = UpdatePhoneNumberForm(request.POST, instance=phone_number)
        if form.is_valid():
            form.save()
            return redirect(
                reverse("phone_number_list")
            )
    else:
        form = UpdatePhoneNumberForm(instance=phone_number)

    return render(
        request,
        "contacts/update/update_phone_number.html",
        {"form": form, "phone_number": phone_number},
    )
