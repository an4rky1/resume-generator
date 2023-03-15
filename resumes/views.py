from django.views.generic import CreateView, DetailView, View
from django.http import HttpResponse
from django.urls import reverse_lazy

from .forms import ResumeForm
from .models import Resume
from .services.pdf_generator import PdfGenerationService


class ResumeCreateView(CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/create.html'
    success_url = reverse_lazy('resumes:create')

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.skills = form.cleaned_data['skills_input']
        resume.experience = form.cleaned_data['experience_input']
        resume.save()
        return super().form_valid(form)


class ResumeDetailView(DetailView):
    model = Resume
    template_name = 'resumes/detail.html'
    context_object_name = 'resume'


class ResumePdfDownloadView(View):
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.get(slug=self.kwargs['slug'])
        html_content = PdfGenerationService.render_resume_html(resume)
        pdf_bytes = PdfGenerationService.generate_pdf(html_content)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.slug}-resume.pdf"'
        return response
