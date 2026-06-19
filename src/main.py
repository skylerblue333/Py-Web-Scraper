from fastapi import FastAPI, HTTPException
from src.scraper import scrape

app = FastAPI(title="Web Scraper API")

@app.get("/scrape")
def scrape_url(url: str):
    try:
        page = scrape(url)
        return {"url": page.url, "title": page.title, "links": page.links}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
