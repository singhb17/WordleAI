# Wordle Solver (Flask)

A web app that helps you solve Wordle-style puzzles. Pick a word length, and the
app suggests guesses and narrows down the candidate list based on the feedback
you enter after each guess. Word lists are fetched at runtime from public
GitHub-hosted JSON word lists (no local database needed).

**How feedback is entered:** for each letter of the suggested word, type the
letter in UPPERCASE if it's in the correct position (green), lowercase if it's
in the word but in the wrong position (yellow), or `-` if it's not in the word
(gray).

**Modes:**
- **From scratch** — the app plays from the first guess.
- **From middle** — you've already made some guesses in a real game; enter them
  along with their feedback and the app picks up from there.

A standalone terminal version is also included (`WordleAI-Terminal.py`).

## Setup

```bash
git clone https://github.com/<your-username>/<this-repo>.git
cd <this-repo>
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

## Environment variables

| Variable     | Required   | Description                                                        |
| ------------ | ---------- | ------------------------------------------------------------------ |
| `SECRET_KEY` | production | Flask session signing key. Falls back to a dev-only value locally. |

Generate a strong value with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Run locally

```bash
python main_flask.py
```

Then open http://127.0.0.1:5000.

## Deploy on Render

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn main_flask:app`
- **Environment:** set `SECRET_KEY` in the Render dashboard (Environment tab).
