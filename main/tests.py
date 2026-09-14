from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Certification


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

class CertificationPageTest(TestCase):
    def setUp(self):
        self.certification = Certification.objects.create(
            title="Belajar Dasar Pemrograman Web",
            issuer="Dicoding Indonesia",
            issued_date="2026-06-01",
            credential_url="https://www.dicoding.com/certificates/example",
        )

    def test_certifications_url_is_accessible(self):
        response = self.client.get(reverse("main:show_certifications"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "certification.html")
        self.assertContains(response, f'href="{reverse("main:show_certifications")}"')

    def test_certification_model(self):
        self.assertEqual(
            str(self.certification),
            "Belajar Dasar Pemrograman Web - Dicoding Indonesia",
        )

    def test_certification_data_appears_on_page(self):
        response = self.client.get(reverse("main:show_certifications"))

        self.assertContains(response, self.certification.title)
        self.assertContains(response, self.certification.issuer)

    def test_empty_certification_page(self):
        Certification.objects.all().delete()
        response = self.client.get(reverse("main:show_certifications"))

        self.assertContains(response, "Belum ada sertifikasi yang ditambahkan.")