import json

from django import forms

from .models import Resume


class ResumeForm(forms.ModelForm):
    skills_input = forms.CharField(
        label='Skills (через запятую)',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Django, Python, PostgreSQL, Docker',
        }),
    )
    experience_input = forms.CharField(
        label='Experience (JSON array)',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': json.dumps([
                {'company': 'Acme Corp', 'role': 'Backend Dev', 'years': '2022-2024'},
                {'company': 'StartupX', 'role': 'Junior Dev', 'years': '2020-2022'},
            ], indent=2),
        }),
    )

    class Meta:
        model = Resume
        fields = ['name', 'bio', 'template_style']

    def clean_skills_input(self):
        raw = self.cleaned_data.get('skills_input', '')
        return [s.strip() for s in raw.split(',') if s.strip()]

    def clean_experience_input(self):
        raw = self.cleaned_data.get('experience_input', '')
        if not raw:
            return []
        try:
            data = json.loads(raw)
            if not isinstance(data, list):
                raise forms.ValidationError('Experience должен быть JSON массивом')
            return data
        except json.JSONDecodeError:
            raise forms.ValidationError(
                'Введите валидный JSON массив. '
                'Пример: [{"company": "Acme", "role": "Dev", "years": "2023"}]'
            )
