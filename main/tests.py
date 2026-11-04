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
        # Halaman dirender lewat AJAX: HTML hanya memuat kerangka, data
        # datang dari endpoint JSON.
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertEqual(len(data), 1)
        fields = data[0]["fields"]
        self.assertEqual(fields["title"], self.experience.title)
        self.assertEqual(fields["description"], self.experience.description)
        self.assertEqual(fields["category_display"], "Part-Time")
        self.assertTrue(fields["is_ongoing"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, 'id="empty"')
        self.assertContains(
            response, "Belum ada pengalaman yang ditambahkan atau ditemukan."
        )
        self.assertEqual(
            self.client.get(reverse("main:get_experiences_json")).json(), []
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)
        self.assertEqual(
            self.client.get(reverse("main:show_experience")).status_code, 200
        )
        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertFalse(data[0]["fields"]["is_ongoing"])


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
        # Halaman memuat daftar lewat API DRF, jadi data diperiksa di API.
        page = self.client.get(reverse("main:show_certifications"))
        self.assertContains(page, 'id="cert-list"')
        self.assertContains(page, reverse("api:certification-list"))

        data = self.client.get(reverse("api:certification-list")).json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.certification.title)
        self.assertEqual(data[0]["issuer"], self.certification.issuer)

    def test_empty_certification_page(self):
        Certification.objects.all().delete()
        page = self.client.get(reverse("main:show_certifications"))

        self.assertContains(page, "Belum ada sertifikasi.")
        self.assertEqual(
            self.client.get(reverse("api:certification-list")).json(), []
        )