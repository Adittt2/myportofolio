from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Aditya",
        "npm": "2506552752",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada bidang consulting dan UI/UX."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Aditya",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)