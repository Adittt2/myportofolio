from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Certification,Experience


class CertificationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = [
            "id", "title", "issuer", "issued_date", "credential_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_issuer(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Issuer cannot be empty.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class ExperienceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source="get_category_display", read_only=True,
    )
    is_ongoing = serializers.BooleanField(read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "started_at"]

    @staticmethod
    def _clean_text(value, label):
        cleaned = strip_tags(value).strip()
        if not cleaned:
            raise serializers.ValidationError(
                f"{label} tidak boleh kosong atau hanya berisi tag HTML."
            )
        return cleaned

    def validate_title(self, value):
        return self._clean_text(value, "Judul pengalaman")

    def validate_description(self, value):
        return self._clean_text(value, "Deskripsi")

    def get_star_count(self, obj):
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return any(u.pk == request.user.pk for u in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(u.username for u in obj.starred_by.all())