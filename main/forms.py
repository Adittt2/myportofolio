from django import forms
from django.forms import ModelForm, TextInput, DateInput, URLInput
from django.forms import Select, Textarea, URLInput, DateTimeInput
from main.models import Experience
from main.models import Certification
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


class CertificationForm(ModelForm):

    class Meta:
        model = Certification
        fields = [
            "title",
            "issuer",
            "issued_date",
            "credential_url",
        ]

        labels = {
            "title": "Nama Sertifikasi",
            "issuer": "Diterbitkan Oleh",
            "issued_date": "Tanggal Terbit",
            "credential_url": "URL Sertifikat",
        }

        widgets = {
            "title": TextInput(
                attrs={"placeholder": "AWS Certified Cloud Practitioner", "maxlength": 255}
            ),
            "issuer": TextInput(
                attrs={"placeholder": "Amazon Web Services"}
            ),
            "issued_date": DateInput(
                attrs={"type": "date"}
            ),
            "credential_url": URLInput(
                attrs={"placeholder": "https://www.credly.com/badges/..."}
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama sertifikasi tidak boleh hanya berisi tag HTML.")
        return title

    def clean_issuer(self):
        issuer = strip_tags(self.cleaned_data["issuer"]).strip()
        if not issuer:
            raise ValidationError("Nama penerbit tidak boleh hanya berisi tag HTML.")
        return issuer

class ExperienceForm(ModelForm):

    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Thumbnail",
            "ended_at": "Tanggal Selesai (kosongkan jika masih berlangsung)",
        }

        widgets = {
            "title": TextInput(
                attrs={"placeholder": "Software Engineer Intern", "maxlength": 255}
            ),
            "description": Textarea(
                attrs={"placeholder": "Ceritakan pengalamanmu", "rows": 3}
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={"placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000"}
            ),
            "ended_at": DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Judul pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()