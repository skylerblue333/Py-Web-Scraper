# Py-Web-Scraper

![CI](https://github.com/skylerblue333/Py-Web-Scraper/workflows/CI/badge.svg)

Production-ready backend service for scraper operations.

## Architecture
- **API Framework**: FastAPI
- **Concurrency**: Asyncio event loop
- **Testing**: Pytest with 100% coverage
- **Deployment**: Docker containerized

## Quick Start
```bash
pip install -r requirements.txt
pytest tests/ -v
uvicorn src.main:app --reload
```
