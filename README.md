# 🧬 Patent Scraper MVP

Minimal Python project for exploring and processing patent data.

## 🚀 Setup

### 1. Install Poetry
```bash
brew install poetry
````

### 2. Install dependencies

```bash
poetry install
```

Creates a virtual environment (if missing) and installs everything in `pyproject.toml`.

### 3. Activate or run

```bash
poetry env activate        # open environment shell
poetry run python main.py  # run a script directly
```

### 4. Run tests

```bash
poetry run pytest -v
```

---

### 🧠 Notes

* Poetry auto-manages virtual environments.
* No need for manual `venv` setup.
* `package-mode = false` keeps this project dependency-only.

Run scripts with:

```bash
poetry run python main.py
```

