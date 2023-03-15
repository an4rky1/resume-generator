from pathlib import Path

from django.conf import settings
from weasyprint import HTML, CSS

FONT_DIR = Path(settings.BASE_DIR) / 'resumes' / 'static' / 'fonts'

FONT_CSS = """
@font-face {
    font-family: 'Inter';
    src: url(%s);
    font-weight: 400;
    font-style: normal;
}
@font-face {
    font-family: 'Inter';
    src: url(%s);
    font-weight: 700;
    font-style: normal;
}
@font-face {
    font-family: 'Inter';
    src: url(%s);
    font-weight: 400;
    font-style: italic;
}
@font-face {
    font-family: 'Inter';
    src: url(%s);
    font-weight: 700;
    font-style: italic;
}
""" % (
    f'file://{FONT_DIR / "Inter-Regular.ttf"}',
    f'file://{FONT_DIR / "Inter-Bold.ttf"}',
    f'file://{FONT_DIR / "Inter-Italic.ttf"}',
    f'file://{FONT_DIR / "Inter-BoldItalic.ttf"}',
)


class PdfGenerationService:
    @staticmethod
    def generate_pdf(html_content: str) -> bytes:
        font_css = CSS(string=FONT_CSS)
        pdf = HTML(string=html_content).write_pdf(stylesheets=[font_css])
        return pdf
