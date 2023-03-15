from django.views.generic import CreateView, DetailView, View
from django.http import HttpResponse

from .models import Resume


class ResumeCreateView(CreateView):
    model = Resume
    fields = ['name', 'bio', 'skills', 'experience', 'template_style']
    template_name = 'resumes/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return self.object.get_absolute_url()


class ResumeDetailView(DetailView):
    model = Resume
    template_name = 'resumes/detail.html'
    context_object_name = 'resume'


class ResumePdfDownloadView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('PDF generation coming in Step 2', content_type='text/plain')
