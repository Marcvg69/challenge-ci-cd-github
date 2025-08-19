# Challenge: CI/CD with GitHub Actions  
**Author:** Marc Van Goolen (solo project)

A tiny Streamlit app with unit tests and a full CI/CD pipeline that simulates **Dev → QA → Prod** using GitHub Actions, Environments, and approvals.

---

## 🎯 Goals

- **CI** runs on pull requests to `main` (lint → security scan → tests + coverage → artifacts).
- **CD** auto-deploys by branch:
  - push to **`dev`** → deploy to **Dev**
  - push to **`qa`** → deploy to **QA**
  - push/merge to **`main`** → deploy to **Prod** (requires approval)
- The app **looks different per environment** (title + background color).
- Manual **Run workflow** (`workflow_dispatch`) is available for CD.

---

## 🧱 Tech Stack

- Python 3.11+, Streamlit  
- pytest, pytest-cov  
- black, flake8, bandit  
- GitHub Actions (separate **CI** and **CD** workflows)

---

## 📁 Repository Structure

~~~
challenge-ci-cd-github/
├─ app/
│  └─ main.py                # Streamlit app (env-aware UI)
├─ tests/
│  └─ test_app.py            # Unit tests for helpers in app/main.py
├─ .github/
│  └─ workflows/
│     ├─ ci.yml              # PR → main: lint, test, artifacts
│     └─ cd.yml              # Dev/QA/Prod deploys + manual trigger
├─ .gitignore
├─ requirements.txt
├─ pyproject.toml
└─ README.md
~~~

---

## ⚙️ Local Environment Setup

~~~bash
# 1) clone
git clone https://github.com/Marcvg69/challenge-ci-cd-github.git
cd challenge-ci-cd-github

# 2) venv
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3) dependencies
python -m pip install -U pip
pip install -r requirements.txt
~~~

### Run the app locally

~~~bash
export APP_ENV=dev             # or: qa | prod
streamlit run app/main.py
# Terminal 1 → DEV on port 8501
APP_ENV=dev streamlit run app/main.py --server.port 8501 --server.headless true

# Terminal 2 → QA on port 8502
APP_ENV=qa  streamlit run app/main.py --server.port 8502 --server.headless true

# Terminal 3 → PROD on port 8503
APP_ENV=prod FAKE_API_KEY=abc123 \
streamlit run app/main.py --server.port 8503 --server.headless true

~~~

- **Dev** → title “Dev Environment”, **green** background  
![Dev UI](<docs/Screenshot 2025-08-19 at 14.27.22.png>)

- **QA** → title “QA Environment”, **yellow** background  
![QA UI](<docs/Screenshot 2025-08-19 at 14.51.30.png>)

- **Prod** → title “Production Environment”, **red** background and secrect present!
![Prod UI](<docs/Screenshot 2025-08-19 at 15.07.25.png>)
---

## ✅ Local Quality Checks

~~~bash
# formatting
black --check .

# linting
flake8 .

# security (informational; CI does not fail on bandit)
bandit -r app -x tests

# tests + coverage
pytest -q --cov=app --cov-report=term-missing
~~~

---

## 🤖 CI: Continuous Integration

**File:** `.github/workflows/ci.yml`

**Triggers**
- `pull_request` → `main` (required)
- optional: daily schedule (07:00 UTC)
- optional: manual **Run workflow** button

**Steps**
- `black --check .`
- `flake8 .`
- `bandit -r app -x tests` *(informational)*
- `pytest` + coverage
- Upload `coverage.xml` & `pytest-results.xml` as artifacts

**How to trigger CI**
- Open a PR: `feature/...` or `fix/...` → **main**

    git checkout -b docs/ci-proof
    date >> README2.md               # small change to trigger PR
    git add README2.md
    git commit -m "docs: update README2 (trigger CI)"
    git push -u origin docs/ci-proof
![CI PR1](<docs/Screenshot 2025-08-19 at 15.37.44.png>)
![CI PR2](<docs/Screenshot 2025-08-19 at 15.34.40.png>)
![CI PR3](<docs/Screenshot 2025-08-19 at 15.37.44.png>)
[CI PR4](docs/bandit-report.zip)
[CI PR 5](docs/coverage-xml.zip)

- Or Actions → **CI** → *Run workflow* 
![alt text](<docs/Screenshot 2025-08-19 at 15.47.42.png>)
---

## 🚀 CD: Continuous Delivery

**File:** `.github/workflows/cd.yml`

**Triggers**
- `push` to `dev`, `qa`, or `main`
- **Manual Run**: Actions → **CD** → *Run workflow* and choose `env` (`dev|qa|prod`)

**Behavior**
- `dev` → runs **deploy-dev**
CD: Deploy to Dev
Goal: Prove branch-based CD. Only deploy-dev runs, and logs show:
🚀 Deployed to 'dev'.
git checkout -b dev
echo "trigger dev $(date -u)" >> .trigger
git add .trigger
git commit -m "ci: trigger dev deploy"
git push -u origin dev
Actions → CD → open latest run.
![alt text](<docs/Screenshot 2025-08-19 at 16.41.31.png>)
![alt text](<docs/Screenshot 2025-08-19 at 16.41.37.png>)
![alt text](<docs/Screenshot 2025-08-19 at 16.41.42.png>)

- `qa` → runs **deploy-qa**
git checkout -b qa
echo "trigger qa $(date -u)" >> .trigger
git add .trigger
git commit -m "ci: trigger qa deploy"
git push -u origin qa


- `main` → runs **deploy-prod** (pauses on **prod** Environment for approval)
Example merge and push to prod README2.md
![CD PROD1](<docs/Screenshot 2025-08-19 at 15.51.42.png>)
![CD PROD2](<docs/Screenshot 2025-08-19 at 15.51.48.png>)
![CD PROD3](<docs/Screenshot 2025-08-19 at 15.52.29.png>)
![CD PROD4](<docs/Screenshot 2025-08-19 at 15.53.13.png>)
![CD PROD5](<docs/Screenshot 2025-08-19 at 15.53.55.png>)


Each job:
- installs minimal deps
- writes a small build artifact
- **checks presence of demo secret** `FAKE_API_KEY` in logs
- prints the required line: `🚀 Deployed to 'environment'`

---

## 🔐 GitHub Environments & Secrets

1. **Create environments** (Repo → Settings → Environments):
   - `dev`, `qa`, `prod` (names must match `cd.yml`)

2. **Require approval for Prod**:
   - In the **prod** environment, enable **Protection rules** → *Required reviewers* (add yourself or a coach)

3. **Demo secret (optional)**:
   - Repo → Settings → **Secrets and variables** → Actions  
   - New secret: **`FAKE_API_KEY`** with any placeholder value  
   - CD logs will show either  
     `FAKE_API_KEY is configured (length: …)` **or** a warning if missing

---

## 🧵 Branch Strategy

- Work on `feat/*` or `fix/*` branches and open **PRs to `main`** → triggers **CI**
- Push to **`dev`** or **`qa`** to trigger **CD** to those environments
- Merge to **`main`** to trigger **Prod**; approve the deployment in the Actions UI

---

## 📦 Requirements

~~~
streamlit==1.36.0
pytest==8.3.3
pytest-cov==5.0.0
black==24.8.0
flake8==7.1.1
bandit==1.7.9

---

## 🆘 Troubleshooting

- **Job skipped?** Ensure your branch matches the job condition or run CD manually with the `env` picker.  
- **Prod stuck?** Approve it in **Actions → the run → Review deployments**.  
- **Secret warning?** Add `FAKE_API_KEY` at repo or environment level.  
- **Tests can’t import `app`?** Make sure `app/main.py` exists and tests import `app.main`.

---

## 📄 License

MIT (or your choice)
