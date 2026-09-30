import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from main.forms import CertificationForm, ExperienceForm
from main.models import Certification, Experience


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login", "Belum ada sesi login / Cookie tidak ditemukan"
    )
    context = {
        "name": "Aditya Hamka Pratama",
        "npm": "2506552752",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada bidang consulting dan UI/UX."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


# Experience 

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = (
        Experience.objects.prefetch_related("starred_by").order_by("-started_at")
    )

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        starred_users = list(experience.starred_by.all())
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.category,
                "category_display": experience.get_category_display(),
                "thumbnail": experience.thumbnail or "",
                "is_ongoing": experience.is_ongoing,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            },
        })

    return JsonResponse(data, safe=False)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Aditya Hamka",
        "title_query": title_query,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def toggle_star_experience(request, experience_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login untuk memberi star."},
            status=401,
        )

    experience = get_object_or_404(Experience, pk=experience_id)

    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
        is_starred = False
    else:
        experience.starred_by.add(request.user)
        is_starred = True

    starred_users = experience.starred_by.all()
    return JsonResponse({
        "is_starred": is_starred,
        "star_count": starred_users.count(),
        "starred_by_names": ", ".join(u.username for u in starred_users),
    })

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Aditya Hamka",
        "form": form,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        updated_experience = form.save(commit=False)
        updated_experience.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Aditya Hamka",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


# Certification

def get_certifications_json(request):
    title_query = request.GET.get("title", "").strip()
    certifications = (
        Certification.objects.prefetch_related("starred_by").order_by("-issued_date")
    )

    if title_query:
        certifications = certifications.filter(title__icontains=title_query)

    data = []
    for certification in certifications:
        starred_users = list(certification.starred_by.all())
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )

        data.append({
            "pk": str(certification.id),
            "fields": {
                "title": certification.title,
                "issuer": certification.issuer,
                "issued_date": certification.issued_date.strftime("%d %B %Y"),
                "credential_url": certification.credential_url or "",
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            },
        })

    return JsonResponse(data, safe=False)


def show_certifications(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Aditya Hamka",
        "title_query": title_query,
        "form": CertificationForm(),
    }
    return render(request, "certification.html", context)


@login_required(login_url="/login/")
def create_certification(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = CertificationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        certification = form.save(commit=False)
        certification.save()
        messages.success(request, "Sertifikasi baru berhasil ditambahkan!")
        return redirect("main:show_certifications")

    context = {
        "name": "Aditya Hamka",
        "form": form,
    }
    return render(request, "certification_form.html", context)

@require_POST
def create_certification_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan sertifikasi."},
            status=403,
        )

    form = CertificationForm(request.POST)
    if form.is_valid():
        certification = form.save()
        return JsonResponse(
            {"message": "Sertifikasi berhasil ditambahkan.", "pk": str(certification.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def toggle_star_certification(request, certification_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login untuk memberi star."},
            status=401,
        )

    certification = get_object_or_404(Certification, pk=certification_id)

    if certification.starred_by.filter(pk=request.user.pk).exists():
        certification.starred_by.remove(request.user)
        is_starred = False
    else:
        certification.starred_by.add(request.user)
        is_starred = True

    starred_users = certification.starred_by.all()
    return JsonResponse({
        "is_starred": is_starred,
        "star_count": starred_users.count(),
        "starred_by_names": ", ".join(u.username for u in starred_users),
    })


@login_required(login_url="/login/")
def update_certification(request, certification_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    certification = get_object_or_404(Certification, pk=certification_id)
    form = CertificationForm(request.POST or None, instance=certification)

    if request.method == "POST" and form.is_valid():
        updated_certification = form.save(commit=False)
        updated_certification.save()
        messages.success(request, "Sertifikasi berhasil diperbarui!")
        return redirect("main:show_certifications")

    context = {
        "name": "Aditya Hamka",
        "form": form,
        "certification": certification,
    }
    return render(request, "certification_form.html", context)


@login_required(login_url="/login/")
def delete_certification(request, certification_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    certification = get_object_or_404(Certification, pk=certification_id)

    if request.method == "POST":
        certification.delete()
        messages.success(request, "Sertifikasi berhasil dihapus!")
        return redirect("main:show_certifications")

    return redirect("main:show_certifications")


# Authentifikasi

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Aditya Hamka",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie(
            "last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return response

    context = {
        "name": "Aditya Hamka",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response