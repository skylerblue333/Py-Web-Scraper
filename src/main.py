"""
Py-Web-Scraper: Web scraping orchestration and scheduling API
"""
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Py-Web-Scraper", version="3.0.0")

class ScrapeJob(BaseModel):
    url: str
    selector: str

jobs = []

@app.post("/api/v1/scrape")
def queue_scrape(job: ScrapeJob):
    if not job.url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")
    jobs.append(job.dict())
    return {"status": "queued", "url": job.url, "queue_size": len(jobs)}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Py-Web-Scraper", "timestamp": int(time.time())}
