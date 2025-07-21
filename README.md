# Azure Cost Analytics Dashboard

This project provides a basic structure for a cross-platform web dashboard that displays Azure resource and cost analytics. It uses a Python backend with Flask and a simple HTML/JavaScript frontend. Authentication is expected to be handled via Azure AD.

> ⚠️ **Work in progress!**  
> This project is still under development. Features may change or break.

## Project Structure

```
backend/    - Flask application and related modules
frontend/   - Static frontend files
static/     - Placeholder for additional static assets
```

## Quick Start

1. Create a virtual environment and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and adjust values as needed.

3. Run the development server:

```bash
python app.py
```

The API will be available at `http://localhost:5000` by default.

## Testing

Basic tests can be executed with:

```bash
pytest
```


