## Steps:
    - create requirements.txt
    - Run: uv venv .venv
    - Run: .venv/Scripts/Activate
    - Run: uv init --bare which creates pyproject.toml
    - Run: uv add -r requirements.txt which adds dependencies to pyproject.toml
    - Run: uv run app.py
