# from fastapi.responses import JSONResponse
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
#
#
#
# app = FastAPI()
# base_url = "http://asilmedia.org/"
#
#
#
#
# @app.get("/multfilmlar/{page_number}", response_class=JSONResponse)
# async def get_multik(page_number: int):
#     url = f"{base_url}films/multfilmlar_multiklar/page/{page_number}/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     results = []
#
#     all_items = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
#     for item in all_items:
#         title = item.find('h2', class_='title is-6 txt-ellipsis mb-2').text.strip()
#         img_src = item.find("img").get("data-src")
#         img_src = urljoin(base_url, img_src) if img_src else None
#
#         a_tag = item.find("a", class_="flx flx-column flx-column-reverse")
#         site_url = a_tag.get("href")
#
#         # Film haqida ma'lumotlarni olish uchun funktsiyani chaqirish
#         film_details = get_multik_details(site_url)
#
#         result = {
#             # "site_url": site_url,
#             "title": title,
#             "img_src": img_src,
#             "more": film_details
#         }
#         results.append(result)
#
#     return results
#
#
# def get_multik_details(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     film_details = {}
#
#     div_element = soup.find("div", class_="full-body mb-4")
#     if div_element:
#         # Agar "la-la-1" nomli div topilsa
#         p_element = div_element.find("p", class_="full-text full-storyimg mb-3")
#         if p_element:
#             film_details["description"] = p_element.text.strip()
#
#         video_element = soup.find("div", class_="downlist-inner flx flx-column")
#         if video_element:
#             a_tags = video_element.find_all("a")
#             video_urls = {}
#             for a_tag in a_tags:
#                 href = a_tag.get("href")
#                 if href and "Скачать" in a_tag.text:
#                     label = a_tag.text.strip().split()[1]
#                     video_urls[label] = urljoin(url, href)
#             film_details["video_urls"] = video_urls
#
#         list_divs = div_element.find_all("div", class_="fullinfo-list mb-2")
#         for list_div in list_divs:
#             a_tags = list_div.find_all("a")
#             if a_tags:
#                 label = list_div.find("span", class_="list-label").text.strip()
#                 label_key = label.lower().replace(":", "")
#                 label_values = [a.text.strip() for a in a_tags]
#                 if label_key == "жанры":
#                     film_details["genres"] = label_values
#                 elif label_key == "режиссер":
#                     film_details["director"] = label_values
#                 elif label_key == "актеры":
#                     film_details["actors"] = label_values
#
#     fullmeta_list = soup.find("div", class_="fullmeta-list flx")
#     if fullmeta_list:
#         fullmeta_items = fullmeta_list.find_all("div", class_="fullmeta-item flx flx-column txt-uppercase")
#         for ok in fullmeta_items:
#             a_tags = ok.find_all("a")
#             if a_tags:
#                 label = ok.find("span", class_="fullmeta-label").text.strip()
#                 label_key = label.lower().replace(":", "")
#                 label_values = [a.text.strip() for a in a_tags]
#                 if label_key == "год":
#                     film_details["year"] = label_values
#                 elif label_key == "страна":
#                     film_details["side"] = label_values
#                 elif label_key == "продолжительность":
#                     film_details["duration"] = label_values
#
#     return film_details
#
#
# @app.get("/filmlar/{page_number}", response_class=JSONResponse)
# async def get_news(page_number: int):
#     url = f"{base_url}/lastnews/page/{page_number}/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     results = []
#
#     all_items = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
#     for item in all_items:
#         title = item.find('h2', class_='title is-6 txt-ellipsis mb-2').text.strip()
#         img_src = item.find("img").get("data-src")
#         img_src = urljoin(base_url, img_src) if img_src else None
#
#         a_tag = item.find("a", class_="flx flx-column flx-column-reverse")
#         site_url = a_tag.get("href")
#
#         # Film haqida ma'lumotlarni olish uchun funktsiyani chaqirish
#         film_details = get_film_details(site_url)
#
#         result = {
#             # "site_url": site_url,
#             "title": title,
#             "img_src": img_src,
#             "more": film_details
#         }
#         results.append(result)
#
#     return results
#
#
#
#
# class SearchRequest(BaseModel):
#     story: str
#
# class SearchResult(BaseModel):
#     title: str
#     img_src: str
#     more: dict  # More field added to include additional details
#
# @app.post("/search", response_model=List[SearchResult])
# async def search_news(request: SearchRequest):
#     query = request.story
#     url = urljoin(base_url, "/lastnews/")
#     payload = {
#         "story": query,
#         "do": "search",
#         "subaction": "search"
#     }
#
#     try:
#         response = requests.post(url, data=payload)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "html.parser")
#
#         results = []
#         all_items = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
#         for item in all_items:
#             title = item.find('h2', class_='title is-6 txt-ellipsis mb-2').text.strip()
#             img_src = item.find("img").get("data-src")
#             img_src = urljoin(base_url, img_src) if img_src else None
#
#             a_tag = item.find("a", class_="flx flx-column flx-column-reverse")
#             site_url = a_tag.get("href")
#
#             # Film haqida ma'lumotlarni olish uchun funktsiyani chaqirish
#             film_details = get_film_details(site_url)
#
#             result = {
#                 "title": title,
#                 "img_src": img_src,
#                 "more": film_details  # Add more details to the result
#             }
#             results.append(result)
#
#         return results
#
#     except requests.RequestException as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
#
#
# def get_film_details(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     film_details = {}
#
#     div_element = soup.find("div", class_="full-body mb-4")
#     if div_element:
#         # Agar "la-la-1" nomli div topilsa
#         p_element = div_element.find("p", class_="full-text full-storyimg mb-3")
#         if p_element:
#             film_details["description"] = p_element.text.strip()
#
#         video_element = soup.find("div", class_="downlist-inner flx flx-column")
#         if video_element:
#             a_tags = video_element.find_all("a")
#             video_urls = {}
#             for a_tag in a_tags:
#                 href = a_tag.get("href")
#                 if href and "Скачать" in a_tag.text:
#                     label = a_tag.text.strip().split()[1]
#                     video_urls[label] = urljoin(url, href)
#             film_details["video_urls"] = video_urls
#
#         list_divs = div_element.find_all("div", class_="fullinfo-list mb-2")
#         for list_div in list_divs:
#             a_tags = list_div.find_all("a")
#             if a_tags:
#                 label = list_div.find("span", class_="list-label").text.strip()
#                 label_key = label.lower().replace(":", "")
#                 label_values = [a.text.strip() for a in a_tags]
#                 if label_key == "жанры":
#                     film_details["genres"] = label_values
#                 elif label_key == "режиссер":
#                     film_details["director"] = label_values
#                 elif label_key == "актеры":
#                     film_details["actors"] = label_values
#
#     fullmeta_list = soup.find("div", class_="fullmeta-list flx")
#     if fullmeta_list:
#         fullmeta_items = fullmeta_list.find_all("div", class_="fullmeta-item flx flx-column txt-uppercase")
#         for ok in fullmeta_items:
#             a_tags = ok.find_all("a")
#             if a_tags:
#                 label = ok.find("span", class_="fullmeta-label").text.strip()
#                 label_key = label.lower().replace(":", "")
#                 label_values = [a.text.strip() for a in a_tags]
#                 if label_key == "год":
#                     film_details["year"] = label_values
#                 elif label_key == "страна":
#                     film_details["side"] = label_values
#                 elif label_key == "продолжительность":
#                     film_details["duration"] = label_values
#
#     return film_details


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

    div_element = soup.find("div", class_="full-body mb-4")
    if div_element:
        # Agar "la-la-1" nomli div topilsa
        p_element = div_element.find("p", class_="full-text full-storyimg mb-3")
        if p_element:
            film_details["description"] = p_element.text.strip()

        video_element = soup.find("div", class_="downlist-inner flx flx-column")
        if video_element:
            a_tags = video_element.find_all("a")
            video_urls = {}
            for a_tag in a_tags:
                href = a_tag.get("href")
                if href and "Скачать" in a_tag.text:
                    label = a_tag.text.strip().split()[1]
                    video_urls[label] = urljoin(url, href)
            film_details["video_urls"] = video_urls

        list_divs = div_element.find_all("div", class_="fullinfo-list mb-2")
        for list_div in list_divs:
            a_tags = list_div.find_all("a")
            if a_tags:
                label = list_div.find("span", class_="list-label").text.strip()
                label_key = label.lower().replace(":", "")
                label_values = [a.text.strip() for a in a_tags]
                if label_key == "жанры":
                    film_details["genres"] = label_values
                elif label_key == "режиссер":
                    film_details["director"] = label_values
                elif label_key == "актеры":
                    film_details["actors"] = label_values

    fullmeta_list = soup.find("div", class_="fullmeta-list flx")
    if fullmeta_list:
        fullmeta_items = fullmeta_list.find_all("div", class_="fullmeta-item flx flx-column txt-uppercase")
        for ok in fullmeta_items:
            a_tags = ok.find_all("a")
            if a_tags:
                label = ok.find("span", class_="fullmeta-label").text.strip()
                label_key = label.lower().replace(":", "")
                label_values = [a.text.strip() for a in a_tags]
                if label_key == "год":
                    film_details["year"] = label_values
                elif label_key == "страна":
                    film_details["side"] = label_values
                elif label_key == "продолжительность":
                    film_details["duration"] = label_values

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
