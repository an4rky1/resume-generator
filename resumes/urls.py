from django.urls import path

from . import views

app_name = 'resumes'

urlpatterns = [
    path('', views.ResumeCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.ResumeDetailView.as_view(), name='detail'),
    path('<slug:slug>/download/', views.ResumePdfDownloadView.as_view(), name='download'),
]
