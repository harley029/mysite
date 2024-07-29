from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from files.forms import FileForm
from files.models import File


def index(request):
    return render(request, "files/index.html", context={"msg": "Files Repository"})


@login_required
def files(request):
    fs = File.objects.filter(user=request.user).all()
    return render(request, "files/files_repo.html", context={"fs": fs})


@login_required
def upload(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect(to="files:files_repo")
    else:
        form = FileForm()
    return render(request, "files/upload.html", context={"form": form})


@login_required
def edit(request, f_id):
    if request.method == "POST":
        desc = request.POST.get("description")
        File.objects.filter(pk=f_id, user=request.user).update(description=desc)
        return redirect(to="files:files_repo")
    f = File.objects.filter(pk=f_id, user=request.user).first()
    return render(request, "files/edit_desc.html", context={"f": f})


@login_required
def remove(request, f_id):
    f = File.objects.filter(pk=f_id, user=request.user)
    file_path: Path = settings.MEDIA_ROOT / str(f.first().path)
    if file_path.exists():
        file_path.unlink()
        f.delete()
        print("Removed file")
    else:
        print("File not removed")

    return redirect(to="files:files_repo")
