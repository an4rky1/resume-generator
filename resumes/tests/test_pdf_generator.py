from resumes.services.pdf_generator import PdfGenerationService


class TestPdfGenerationService:
    def test_generate_pdf_returns_bytes(self):
        html = '<html><body><h1 style="font-family: Inter, sans-serif;">Test Resume</h1></body></html>'
        pdf_bytes = PdfGenerationService.generate_pdf(html)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF')
