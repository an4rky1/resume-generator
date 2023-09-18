# Resume Generator

Minimalist resume card generator in the style of Swiss posters from the 60s. Full asymmetry, rigid modular grid, huge contrast text, limited palette.

## Features

- **Constructor form** — enter name, bio, skills (comma-separated), experience (pipe-separated), and pick one of 3 Swiss templates
- **PDF generation** — backend renders HTML with inline styles and streams a print-ready A4 PDF with embedded Inter font
- **Public URLs** — each resume gets a unique slug-based link for sharing
- **3 templates**: Minimal Grid, Bold Asymmetric, Classic Swiss

## Tech Stack

- Django 6
- WeasyPrint (PDF generation)
- Tailwind CSS + Alpine.js (frontend)
- Inter font (embedded in PDF)

## Local Development

### Prerequisites

- Python 3.12+
- Nix (for WeasyPrint system dependencies on NixOS/Nix)

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
```

### Running with Nix (for WeasyPrint support)

If you're on NixOS or use Nix:

```bash
nix-shell
source .venv/bin/activate
python manage.py runserver
```

### Tests

```bash
nix-shell --run "source .venv/bin/activate && python -m pytest resumes/tests/ -v"
```

## Deployment (Fly.io)

```bash
# Install flyctl, then:
flyctl launch --no-deploy

# Set secrets
flyctl secrets set DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"

# Deploy
flyctl deploy
```

For production, set a PostgreSQL database:

```bash
flyctl postgres create
flyctl postgres attach <app-name>
flyctl deploy
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | (must set in prod) |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection string | (uses SQLite) |

## Project Structure

```
├── config/                 # Django settings
├── resumes/
│   ├── forms.py            # Form with validation
│   ├── models.py           # Resume model
│   ├── urls.py             # Routes
│   ├── views.py            # Controllers
│   ├── services/
│   │   └── pdf_generator.py # WeasyPrint service
│   ├── templates/resumes/  # HTML templates
│   │   ├── base.html
│   │   ├── create.html
│   │   ├── detail.html
│   │   └── pdf/            # PDF templates
│   │       ├── minimal.html
│   │       ├── bold.html
│   │       └── classic.html
│   ├── static/fonts/       # Inter font files
│   └── tests/
├── Dockerfile
├── fly.toml
├── requirements.txt
└── shell.nix
```
