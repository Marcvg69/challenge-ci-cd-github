# Challenge: CI/CD with GitHub Actions

A tiny Streamlit app + tests + GitHub Actions that simulate Dev → QA → Prod deployments.

## What’s inside
- `app/main.py` — Streamlit app. Environment styles: Dev (green), QA (yellow), Prod (red).
- `tests/test_app.py` — Unit tests.
- `.github/workflows/ci.yml` — CI on PRs to **main** + daily schedule.
- `.github/workflows/cd.yml` — CD on branch pushes: Dev (dev), QA (qa), Prod (main; requires approval).
- `requirements.txt`, `pyproject.toml`, `.gitignore`.

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APP_ENV=dev        # qa | prod
streamlit run app/main.py
