import app.main as app


def test_normalize_env_defaults_to_dev():
    assert app.normalize_env(None) == "dev"
    assert app.normalize_env("") == "dev"
    assert app.normalize_env("unknown") == "dev"


def test_theme_for_each_env():
    for env in ["dev", "qa", "prod"]:
        t = app.theme_for_env(env)
        assert "title" in t and "bg" in t and "accent" in t
        assert isinstance(t["title"], str) and t["title"]
