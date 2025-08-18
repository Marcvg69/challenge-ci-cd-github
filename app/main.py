import os
import streamlit as st


# ---- small helpers (unit-testable) ----
def normalize_env(value: str | None) -> str:
    v = (value or "").strip().lower()
    return v if v in {"dev", "qa", "prod"} else "dev"


def theme_for_env(env: str) -> dict:
    """Return title and CSS color per environment."""
    env = normalize_env(env)
    mapping = {
        "dev": {"title": "Dev Environment", "bg": "#e6ffed", "accent": "#1f8a36"},
        "qa": {"title": "QA Environment", "bg": "#fff9db", "accent": "#a37b00"},
        "prod": {"title": "Production Environment", "bg": "#ffe6e6", "accent": "#b00020"},
    }
    return mapping[env]


# ---- app ----
APP_ENV = normalize_env(os.getenv("APP_ENV"))
meta = theme_for_env(APP_ENV)
TITLE, BG, ACCENT = meta["title"], meta["bg"], meta["accent"]

st.set_page_config(page_title=TITLE, page_icon="🚀", layout="centered")

# simple CSS theme based on environment
st.markdown(
    f"""
    <style>
      .stApp {{
        background: {BG};
      }}
      .env-badge {{
        display:inline-block; padding:4px 8px; border-radius:6px;
        color: white; background:{ACCENT}; font-weight:600; letter-spacing:.3px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(TITLE)
st.markdown(f'<span class="env-badge">{APP_ENV.upper()}</span>', unsafe_allow_html=True)

st.write(
    "This is a tiny Streamlit sample app used for CI/CD pipeline demos. "
    "It changes style and title depending on the deployment environment."
)

# Optional: show build info from CI
commit = os.getenv("GITHUB_SHA", "local-run")
st.caption(f"Build: {commit[:7]}  •  Environment: {APP_ENV}")

# Optional: demonstrate a secret without printing it
has_secret = bool(os.getenv("FAKE_API_KEY"))
st.write("Secret present:", "✅" if has_secret else "❌")
