# Azure Cost Analytics Dashboard

This project provides a basic structure for a cross-platform web dashboard that displays Azure resource and cost analytics. It uses a Python backend with FastAPI and a simple HTML/JavaScript frontend. Authentication is expected to be handled via Azure AD.

## Project Structure

```
backend/    - FastAPI application and related modules
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
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

## Testing

Basic tests can be executed with:

```bash
pytest
```

