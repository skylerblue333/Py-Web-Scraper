# Py-Web-Scraper

A production-ready web scraper microservice built with FastAPI.

## Features
- Extracts page title and all external links from any URL
- REST API with `/scrape?url=<url>` endpoint
- Fully tested with pytest

## Quick Start

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Docker

```bash
docker build -t py-web-scraper .
docker run -p 8000:8000 py-web-scraper
```

## Test

```bash
pytest tests/ -v
```
