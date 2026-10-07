# Snap & Study

A simple Streamlit study buddy powered by Gemini.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` and add:

```toml
GEMINI_API_KEY = "your-api-key"
```

Run:

```bash
streamlit run app.py
```

The app will open at http://localhost:8501.
