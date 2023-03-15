import uuid

from django.db import models
from django.urls import reverse


class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('minimal', 'Minimal Grid'),
        ('bold', 'Bold Asymmetric'),
        ('classic', 'Classic Swiss'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    bio = models.TextField(max_length=500, blank=True, default='')
    skills = models.JSONField(default=list, blank=True)
    experience = models.JSONField(default=list, blank=True)
    template_style = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='minimal')
    slug = models.SlugField(max_length=160, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = '-'.join(self.name.lower().split())
            slug = base_slug
            counter = 1
            while Resume.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('resumes:detail', kwargs={'slug': self.slug})
