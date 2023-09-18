import json

from django.test import TestCase
from django.urls import reverse

from resumes.models import Resume
from resumes.services.pdf_generator import PdfGenerationService


class TestPdfGenerationService:
    def test_generate_pdf_returns_bytes(self):
        html = '<html><body><h1 style="font-family: Inter, sans-serif;">Test Resume</h1></body></html>'
        pdf_bytes = PdfGenerationService.generate_pdf(html)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF')


class ResumeFormTests(TestCase):
    def test_create_resume_saves_to_db(self):
        response = self.client.post(reverse('resumes:create'), {
            'name': 'John Doe',
            'bio': 'Backend developer',
            'skills_input': 'Python, Django',
            'experience_input': 'Acme | Dev | 2023',
            'template_style': 'minimal',
        })
        assert Resume.objects.count() == 1
        resume = Resume.objects.first()
        assert resume.name == 'John Doe'
        assert resume.skills == ['Python', 'Django']
        assert resume.experience == [{'company': 'Acme', 'role': 'Dev', 'years': '2023'}]
        assert resume.slug is not None

    def test_pdf_download_returns_pdf(self):
        resume = Resume.objects.create(
            name='Jane Smith',
            bio='Designer',
            skills=['Figma', 'CSS'],
            experience=[],
            template_style='bold',
        )
        response = self.client.get(reverse('resumes:download', kwargs={'slug': resume.slug}))
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'
        assert response.content.startswith(b'%PDF')
