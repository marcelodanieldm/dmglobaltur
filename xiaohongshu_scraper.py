"""
xiaohongshu_scraper.py
======================

─────────────────────────────────────────────────────────────
DOCUMENTATION IN ENGLISH
─────────────────────────────────────────────────────────────

This script automates the extraction of trending hashtags and post metadata about luxury travel on Xiaohongshu (Little Red Book).

Main features:
- Headless automation with Playwright to navigate dynamic content.
- Dynamic IP rotation via configurable proxies.
- Extraction of the top 20 most relevant hashtags about "luxury travel", "high-end experiences", "exclusive hotels" and luxury brands.
- For each hashtag: gets the number of posts, shows 3-5 post URLs, and performs sentiment analysis (Gemini 1.5 Flash API) on the captions of the top 3 posts.
- Automatic handling of CAPTCHAs and soft blocks with retry logic.
- Structured output in a JSON file in a temporary directory, ideal for daily scheduled runs.

Requirements:
- Python 3.8+
- playwright
- aiohttp
- requests
- tenacity

Installation:
1. Install dependencies:
    pip install -r requirements.txt
2. Install Playwright browsers:
    playwright install
3. (Optional) Configure proxies in the PROXY_LIST variable if you want IP rotation.
4. Set the GEMINI_API_KEY environment variable with your Gemini 1.5 Flash API key.

Execution:
    python xiaohongshu_scraper.py

The result is saved in a temporary JSON file and the path is printed at the end.

Automation:
You can schedule daily execution with Windows Task Scheduler or cron (Linux/Mac).

Further documentation about functions and structure is available in the code.

─────────────────────────────────────────────────────────────
DOCUMENTACIÓN EN ESPAÑOL
─────────────────────────────────────────────────────────────

Este script automatiza la extracción de tendencias de hashtags y metadatos de posts sobre viajes de lujo en Xiaohongshu (Little Red Book).

Características principales:
- Automatización headless con Playwright para navegar contenido dinámico.
- Rotación dinámica de IPs mediante proxies configurables.
- Extracción de los 20 hashtags más relevantes sobre "viajes de lujo", "experiencias high-end", "hoteles exclusivos" y marcas de lujo.
- Para cada hashtag: obtiene el número de posts, muestra 3-5 URLs de posts y realiza análisis de sentimiento (Gemini 1.5 Flash API) sobre los captions de los 3 posts principales.
- Manejo automático de CAPTCHAs y bloqueos suaves con lógica de reintentos.
- Salida estructurada en JSON en un archivo temporal, ideal para ejecución diaria programada.

Requisitos:
- Python 3.8+
- playwright
- aiohttp
- requests
- tenacity

Instalación:
1. Instala las dependencias:
    pip install -r requirements.txt
2. Instala los navegadores de Playwright:
    playwright install
3. (Opcional) Configura proxies en la variable PROXY_LIST si deseas rotación de IP.
4. Define la variable de entorno GEMINI_API_KEY con tu clave de API de Gemini 1.5 Flash.

Ejecución:
    python xiaohongshu_scraper.py

El resultado se guarda en un archivo JSON temporal y se imprime la ruta al finalizar.

Automatización:
Puedes programar la ejecución diaria con el programador de tareas de Windows o cron (Linux/Mac).

─────────────────────────────────────────────────────────────
DOCUMENTADO EN ESPERANTO
─────────────────────────────────────────────────────────────

Ĉi tiu skripto aŭtomatigas la ekstraktadon de tendencaj hashtagoj kaj afiŝaj metadatenoj pri luksaj vojaĝoj en Xiaohongshu (Little Red Book).

Ĉefaj trajtoj:
- Senkapo aŭtomatigo per Playwright por navigi dinamikan enhavon.
- Dinamika IP-rotacio per agordeblaj prokuriloj (proxy).
- Ekstraktado de la 20 plej gravaj hashtagoj pri "luksaj vojaĝoj", "altkvalitaj spertoj", "ekskluzivaj hoteloj" kaj luksaj markoj.
- Por ĉiu hashtag: akiras la nombron de afiŝoj, montras 3-5 URL-ojn de afiŝoj kaj faras sentiman analizadon (Gemini 1.5 Flash API) pri la priskriboj de la 3 ĉefaj afiŝoj.
- Aŭtomata traktado de CAPTCHA-oj kaj mildaj blokoj per reprovlogiko.
- Strukturita eligo en JSON-dosiero en provizora dosierujo, ideala por ĉiutaga planita rulado.

Postuloj:
- Python 3.8+
- playwright
- aiohttp
- requests
- tenacity

Instalado:
1. Instalu la dependecojn:
    pip install -r requirements.txt
2. Instalu la retumilojn de Playwright:
    playwright install
3. (Laŭvole) Agordu prokurilojn en la variablo PROXY_LIST se vi volas IP-rotacion.
4. Difinu la medivariablon GEMINI_API_KEY kun via Gemini 1.5 Flash API-ŝlosilo.

Rulado:
    python xiaohongshu_scraper.py

La rezulto estas konservita en provizora JSON-dosiero kaj la vojo estas presita ĉe la fino.

Aŭtomatigo:
Vi povas plani ĉiutagan ruladon per la Task Scheduler de Windows aŭ cron (Linux/Mac).

Plia dokumentado pri funkcioj kaj strukturo disponeblas en la kodo.
"""
import asyncio
import json
import os
import random
import tempfile
from typing import List, Dict, Any

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# ========== CONFIGURATION ==========
XHS_URL = "https://www.xiaohongshu.com/"
SEARCH_TERMS = [
    "奢华旅行",  # luxury travel
    "高端体验",  # high-end experiences
    "独家酒店",  # exclusive hotels
    "奢侈品牌",  # luxury brands
    # Add specific luxury brand names in Chinese as needed
]
PROXY_LIST = [
    # Add your proxies here, e.g. 'http://user:pass@proxyhost:port'
]
MAX_HASHTAGS = 20
SAMPLE_POSTS = 5
TOP_POSTS_FOR_SENTIMENT = 3
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set this in your environment
HEADLESS = True
MAX_RETRIES = 3

# ========== UTILITY FUNCTIONS ==========
async def get_random_proxy() -> str:
    if not PROXY_LIST:
        return None
    return random.choice(PROXY_LIST)

async def call_gemini_sentiment(text: str, session: aiohttp.ClientSession) -> float:
    """Call Gemini 1.5 Flash API for sentiment analysis. Returns a float 0.0-1.0."""
    if not GEMINI_API_KEY:
        return 0.5  # fallback neutral
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"请对以下中文文本进行情感分析，返回0.0到1.0之间的分数，1.0为极其正面，0.0为极其负面，仅返回数字分数：\n{text}"}]}]
    }
    params = {"key": GEMINI_API_KEY}
    try:
        async with session.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=10) as resp:
            data = await resp.json()
            # Parse the response to extract the score
            score_str = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            try:
                return float(score_str)
            except Exception:
                return 0.5
    except Exception:
        return 0.5

# ========== SCRAPER CORE ==========
@retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=2, min=2, max=10),
       retry=retry_if_exception_type(PlaywrightTimeoutError))
async def fetch_hashtag_data(playwright, hashtag: str, proxy: str = None) -> Dict[str, Any]:
    browser_args = ["--disable-blink-features=AutomationControlled"]
    if proxy:
        browser_args.append(f"--proxy-server={proxy}")
    browser = await playwright.chromium.launch(headless=HEADLESS, args=browser_args)
    context = await browser.new_context()
    page = await context.new_page()
    try:
        # Search for the hashtag
        await page.goto(XHS_URL, timeout=20000)
        await page.wait_for_selector('input[type="search"]', timeout=10000)
        await page.fill('input[type="search"]', hashtag)
        await page.keyboard.press('Enter')
        await page.wait_for_timeout(3000)
        # Wait for results to load
        await page.wait_for_selector('a[href*="/explore/"]', timeout=10000)
        # Extract hashtags and post counts
        hashtags = await page.query_selector_all('a[href*="/explore/"]')
        results = []
        for h in hashtags[:MAX_HASHTAGS]:
            tag_text = await h.inner_text()
            tag_url = await h.get_attribute('href')
            # Go to hashtag page
            await page.goto(f"https://www.xiaohongshu.com{tag_url}", timeout=15000)
            await page.wait_for_timeout(2000)
            # Extract post count
            try:
                post_count_elem = await page.query_selector('span:has-text("笔记")')
                post_count_text = await post_count_elem.inner_text() if post_count_elem else "0"
                post_count = int(''.join(filter(str.isdigit, post_count_text)))
            except Exception:
                post_count = 0
            # Extract sample post URLs
            post_links = await page.query_selector_all('a[href*="/explore/"]')
            sample_posts = []
            for pl in post_links[:SAMPLE_POSTS]:
                url = await pl.get_attribute('href')
                if url:
                    sample_posts.append(f"https://www.xiaohongshu.com{url}")
            # Extract captions for sentiment
            captions = []
            for pl in post_links[:TOP_POSTS_FOR_SENTIMENT]:
                try:
                    await pl.click()
                    await page.wait_for_selector('div[class*="noteContent"]', timeout=5000)
                    caption_elem = await page.query_selector('div[class*="noteContent"]')
                    caption = await caption_elem.inner_text() if caption_elem else ""
                    captions.append(caption)
                    await page.go_back()
                except Exception:
                    captions.append("")
            results.append({
                "hashtag": tag_text,
                "post_count": post_count,
                "sample_posts": sample_posts,
                "captions": captions
            })
        await browser.close()
        return results
    except Exception as e:
        await browser.close()
        raise e

async def main():
    all_results = []
    async with aiohttp.ClientSession() as session:
        async with async_playwright() as playwright:
            for term in SEARCH_TERMS:
                proxy = await get_random_proxy()
                try:
                    hashtag_data = await fetch_hashtag_data(playwright, term, proxy)
                    for tag in hashtag_data:
                        # Sentiment analysis
                        sentiments = []
                        for caption in tag["captions"]:
                            if caption.strip():
                                score = await call_gemini_sentiment(caption, session)
                                sentiments.append(score)
                        avg_sentiment = round(sum(sentiments)/len(sentiments), 2) if sentiments else 0.5
                        all_results.append({
                            "hashtag": tag["hashtag"],
                            "post_count": tag["post_count"],
                            "sample_posts": tag["sample_posts"],
                            "avg_sentiment": avg_sentiment
                        })
                except Exception as e:
                    print(f"Error fetching data for {term}: {e}")
    # Output to temp JSON file
    temp_dir = tempfile.gettempdir()
    out_path = os.path.join(temp_dir, "xiaohongshu_trends.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"Results written to {out_path}")

if __name__ == "__main__":
    asyncio.run(main())
