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
        label='Experience (каждая строка: Компания | Должность | Годы)',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Acme Corp | Backend Developer | 2022-2024\nStartupX | Junior Dev | 2020-2022',
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
        if not raw.strip():
            return []
        result = []
        for line in raw.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 2:
                raise forms.ValidationError(
                    f'Строка "{line}" должна быть в формате: Компания | Должность | Годы'
                )
            result.append({
                'company': parts[0],
                'role': parts[1],
                'years': parts[2] if len(parts) > 2 else '',
            })
        return result
