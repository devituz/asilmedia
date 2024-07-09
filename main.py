from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import aiohttp
import asyncio
from cachetools import TTLCache
from urllib.parse import urljoin

from bs4 import BeautifulSoup  # BeautifulSoup ni import qilib olish


app = FastAPI()

base_url = "http://asilmedia.org/"
cache = TTLCache(maxsize=100, ttl=3600)  # 1 soatlik kesh

class SearchRequest(BaseModel):
    story: str

class SearchResult(BaseModel):
    title: str
    img_src: str
    more: dict  # More field added to include additional details

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

@app.get("/multfilmlar/{page_number}", response_class=JSONResponse)
async def get_multik(page_number: int):
    cache_key = f"multfilmlar_{page_number}"
    if cache_key in cache:
        return cache[cache_key]

    url = f"{base_url}films/multfilmlar_multiklar/page/{page_number}/"
    content = await fetch(url)
    soup = BeautifulSoup(content, "html.parser")
    results = []

    all_items = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
    tasks = [parse_multik_item(item) for item in all_items]
    results = await asyncio.gather(*tasks)

    cache[cache_key] = results
    return results

async def parse_multik_item(item):
    title = item.find('h2', class_='title is-6 txt-ellipsis mb-2').text.strip()
    img_src = item.find("img").get("data-src")
    img_src = urljoin(base_url, img_src) if img_src else None

    a_tag = item.find("a", class_="flx flx-column flx-column-reverse")
    site_url = a_tag.get("href")

    film_details = await fetch_multik_details(site_url)

    return {
        "title": title,
        "img_src": img_src,
        "more": film_details
    }

async def fetch_multik_details(url):
    content = await fetch(url)
    soup = BeautifulSoup(content, "html.parser")
    film_details = {}
    # Parsing logic remains the same
    # ...

    return film_details

@app.get("/filmlar/{page_number}", response_class=JSONResponse)
async def get_news(page_number: int):
    cache_key = f"filmlar_{page_number}"
    if cache_key in cache:
        return cache[cache_key]

    url = f"{base_url}/lastnews/page/{page_number}/"
    content = await fetch(url)
    soup = BeautifulSoup(content, "html.parser")
    results = []

    all_items = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
    tasks = [parse_news_item(item) for item in all_items]
    results = await asyncio.gather(*tasks)

    cache[cache_key] = results
    return results

async def parse_news_item(item):
    title = item.find('h2', class_='title is-6 txt-ellipsis mb-2').text.strip()
    img_src = item.find("img").get("data-src")
    img_src = urljoin(base_url, img_src) if img_src else None

    a_tag = item.find("a", class_="flx flx-column flx-column-reverse")
    site_url = a_tag.get("href")

    film_details = await fetch_film_details(site_url)

    return {
        "title": title,
        "img_src": img_src,
        "more": film_details
    }

async def fetch_film_details(url):
    content = await fetch(url)
    soup = BeautifulSoup(content, "html.parser")
    film_details = {}
    # Parsing logic remains the same
    # ...

    return film_details

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
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as response:
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")

                results = []
                all_items = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
                tasks = [parse_news_item(item) for item in all_items]
                results = await asyncio.gather(*tasks)

                return results

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
