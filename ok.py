from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI()

base_url = "http://asilmedia.org/"

class SearchRequest(BaseModel):
    story: str

class SearchResult(BaseModel):
    title: str
    img_src: str

@app.post("/search", response_model=List[SearchResult])
async def search_news(request: SearchRequest):
    query = request.story
    url = urljoin(base_url, "/lastnews/")
    payload = {
        "story": query,
        "do": "search",
        "subaction": "search"
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        results = []
        all_items = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
        for item in all_items:
            title = item.find('h2', class_='title is-6 txt-ellipsis mb-2').text.strip()
            img_src = item.find("img").get("data-src")
            img_src = urljoin(base_url, img_src) if img_src else None

            result = {
                "title": title,
                "img_src": img_src
            }
            results.append(result)

        return results

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
