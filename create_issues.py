#!/usr/bin/env python3
"""
Create GitHub issues for analytics-server improvements.

Usage:
    # Using a GitHub personal access token:
    GITHUB_TOKEN=ghp_xxx python3 create_issues.py

    # Or using gh CLI (if authenticated):
    pip install PyGithub  # if not installed
    GITHUB_TOKEN=$(gh auth token) python3 create_issues.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

REPO = "slevin48/analytics-server"
API_URL = f"https://api.github.com/repos/{REPO}/issues"

ISSUES = [
    {
        "title": "Fix path traversal vulnerability in dataset endpoints",
        "labels": ["bug", "security"],
        "body": """## Priority: Critical

In `app/main.py`, endpoints use raw string concatenation with user input:

```python
pd.read_csv("data/"+dataset_name)  # line 25
```

An attacker can request `/api/dataset/../../etc/passwd` to read arbitrary files on the server.

### Fix
Use `pathlib.Path` and validate the resolved path stays within the `data/` directory:

```python
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def safe_dataset_path(dataset_name: str) -> Path:
    path = (DATA_DIR / dataset_name).resolve()
    if not path.is_relative_to(DATA_DIR.resolve()):
        raise HTTPException(status_code=400, detail="Invalid dataset name")
    return path
```

This affects the GET (`/api/dataset/{dataset_name}`), POST, and DELETE endpoints.
""",
    },
    {
        "title": "Remove dead Flask code and unused dependencies",
        "labels": ["cleanup"],
        "body": """## Cleanup

`app/flask_server.py` and the `connexion`/`flask` dependencies are leftover from the pre-FastAPI migration (PR #1). They are not used anywhere in the current application.

### Tasks
- [ ] Delete `app/flask_server.py`
- [ ] Remove `connexion` from `Pipfile` and `requirements.txt`
- [ ] Remove `flask` from `Pipfile` and `requirements.txt`
- [ ] Evaluate whether `app/swagger.yml` is still needed (it was used by connexion, not FastAPI)
- [ ] Regenerate `Pipfile.lock`
""",
    },
    {
        "title": "Add error handling to all API endpoints",
        "labels": ["enhancement"],
        "body": """## Problem

There are no `try/except` blocks anywhere in the codebase. All failure modes produce raw 500 errors with stack traces:

- Requesting a non-existent dataset → unhandled `FileNotFoundError`
- Uploading a malformed CSV → unhandled pandas `ParserError`
- Deleting a non-existent dataset → unhandled `FileNotFoundError` from `os.remove()`
- Invalid file operations → unhandled `OSError`/`PermissionError`

### Tasks
- [ ] Return `404` when a requested dataset doesn't exist
- [ ] Return `400` when an uploaded file is not valid CSV
- [ ] Return `409` or `400` when uploading a dataset that already exists (or decide on overwrite behavior)
- [ ] Return `404` when deleting a non-existent dataset
- [ ] Add a global exception handler for unexpected errors that returns a clean JSON response instead of a stack trace
- [ ] Add input validation for filenames (reject special characters, enforce `.csv` extension)
- [ ] Add file size limits to the upload endpoint
""",
    },
    {
        "title": "Bump Python to 3.11+ and update deprecated dependencies",
        "labels": ["enhancement"],
        "body": """## Problem

The project targets **Python 3.7**, which reached end-of-life in June 2023. Several dependencies and code patterns are outdated.

### Tasks
- [ ] Update `Pipfile` to require Python 3.11+
- [ ] Update `Dockerfile` base image from `tiangolo/uvicorn-gunicorn-fastapi:python3.7` to a current Python version
- [ ] Replace deprecated `df.append()` in `app/dataset.py:20` with `pd.concat()`
- [ ] Update `fastapi` from 0.63.0 to latest
- [ ] Update `aiofiles` from 0.6.0 to latest
- [ ] Update all other pinned dependencies to current versions
- [ ] Consider migrating from `Pipfile` to `pyproject.toml` with a modern tool (uv, hatch, or poetry)
- [ ] Fix mixed-content CSS import in `app/static/css/home.css` (`http://` → `https://` for Google Fonts)
- [ ] Regenerate lock file after updates
- [ ] Test that the application still runs correctly after all upgrades
""",
    },
    {
        "title": "Add test suite with pytest and FastAPI TestClient",
        "labels": ["testing"],
        "body": """## Problem

The project has **zero test coverage**. There are no tests of any kind.

### Tasks
- [ ] Add `pytest` and `httpx` to dev dependencies
- [ ] Create `tests/` directory structure
- [ ] Write tests for each endpoint:
  - `GET /` — returns HTML homepage
  - `GET /api/dataset` — returns list of datasets with metadata
  - `GET /api/dataset/{name}` — returns CSV data as JSON
  - `POST /api/dataset` — uploads a new CSV file
  - `DELETE /api/dataset/{name}` — removes a dataset
- [ ] Add edge case tests:
  - Request non-existent dataset
  - Upload invalid file
  - Delete non-existent dataset
  - Path traversal attempts (security regression tests)
- [ ] Add a `conftest.py` with fixtures (test client, sample CSV data, temp data directory)
- [ ] Ensure tests use a temporary data directory, not the real `app/data/`
- [ ] Add a test configuration section to `pyproject.toml` or `pytest.ini`
""",
    },
    {
        "title": "Add GitHub Actions CI workflow for linting and testing",
        "labels": ["enhancement"],
        "body": """## Problem

There is no CI/CD pipeline. No linter or formatter is configured. Regressions can be introduced without any automated checks.

### Tasks
- [ ] Add `ruff` as a dev dependency for linting and formatting
- [ ] Create a `ruff.toml` or add `[tool.ruff]` section to `pyproject.toml`
- [ ] Create `.github/workflows/ci.yml` with:
  - Lint step (`ruff check .`)
  - Format check step (`ruff format --check .`)
  - Test step (`pytest`)
  - Run on push and pull requests to `master`
- [ ] Fix any existing lint violations
- [ ] Optionally add a Docker build step to verify the image builds successfully
""",
    },
    {
        "title": "Implement or remove incomplete frontend CRUD operations",
        "labels": ["bug", "enhancement"],
        "body": """## Problem

`app/static/js/home.js` has a model/view/controller pattern, but `model.create`, `model.update`, and `model.delete` are **undefined**. The UI has event handlers wired up for create, update, and delete actions that reference these missing methods — meaning those buttons silently fail.

### Options

**Option A: Implement the missing methods**
- [ ] Add `model.create()` — POST to `/api/dataset` with file upload
- [ ] Add `model.update()` — implement dataset rename or content update
- [ ] Add `model.delete()` — DELETE to `/api/dataset/{name}`
- [ ] Add confirmation dialogs before destructive operations
- [ ] Add success/error feedback in the UI after each operation
- [ ] Add a file upload form to the homepage

**Option B: Remove the dead UI code**
- [ ] Remove the unused event handlers and controller methods
- [ ] Simplify the frontend to be read-only (list + view datasets)
- [ ] Keep it consistent with the actual working functionality

### Additional frontend improvements (either option)
- [ ] Update jQuery from 3.3.1 to latest, or replace with vanilla JS fetch API
- [ ] Fix the double-click edit handler (currently incomplete)
""",
    },
    {
        "title": "Add authentication to API endpoints",
        "labels": ["enhancement", "security"],
        "body": """## Problem

All API endpoints are completely open. Anyone who can reach the server can upload arbitrary files or delete any dataset. This is a significant risk if the server is exposed beyond localhost.

### Options

**Option A: API key authentication (simplest)**
- [ ] Add API key middleware that checks an `X-API-Key` header or query parameter
- [ ] Store the API key in an environment variable
- [ ] Apply auth to mutating endpoints (POST, DELETE) at minimum
- [ ] Keep GET endpoints open or optionally protected
- [ ] Return `401 Unauthorized` for missing/invalid keys

**Option B: OAuth2 / JWT (more robust)**
- [ ] Add `python-jose` and `passlib` dependencies
- [ ] Implement token-based authentication
- [ ] Add user registration and login endpoints
- [ ] Use FastAPI's built-in OAuth2 security scheme (appears in Swagger UI)

### Recommendation
Start with **Option A** (API key) for simplicity. It covers the main risk (unauthorized writes) with minimal complexity. Upgrade to Option B if multi-user support is needed later.

### Additional tasks
- [ ] Add CORS configuration to restrict which origins can call the API
- [ ] Document the authentication method in the README
- [ ] Add rate limiting to prevent abuse
""",
    },
]


def create_issues(token: str) -> None:
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "analytics-server-issue-creator",
    }

    created = 0
    for i, issue in enumerate(ISSUES, 1):
        data = json.dumps(issue).encode()
        req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")

        try:
            resp = urllib.request.urlopen(req)
            result = json.loads(resp.read())
            print(f"  [{i}/8] Created: #{result['number']} - {issue['title']}")
            created += 1
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"  [{i}/8] Failed: {issue['title']}")
            print(f"         HTTP {e.code}: {error_body[:200]}")

    print(f"\nDone: {created}/8 issues created.")
    print(f"View at: https://github.com/{REPO}/issues")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable is required.")
        print("Usage: GITHUB_TOKEN=ghp_xxx python3 create_issues.py")
        sys.exit(1)

    print(f"Creating 8 issues on {REPO}...")
    create_issues(token)
