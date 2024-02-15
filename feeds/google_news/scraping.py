import asyncio
import aiohttp
import feedparser

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def scrape_google_news_rss(search_term):
    url = f"https://news.google.com/news?q={search_term}&output=rss"
    content = await fetch(url)

    feed = feedparser.parse(content)
    scraped_data = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        publication_date = entry.published

        img_url = None
        if 'media_content' in entry:
            img_url = entry.media_content[0]['url']
        elif 'enclosures' in entry:
            img_url = entry.enclosures[0]['href']

        article_info = {
            'title': title,
            'link': link,
            'publication_date': publication_date,
            'img_url': img_url
        }

        scraped_data.append(article_info)

    return scraped_data

# Define el término de búsqueda aquí
search_term = "inteligencia artificial"

# Ejecutar la función asíncrona principal y obtener los datos
if __name__ == "__main__":
    scraped_news = asyncio.run(scrape_google_news_rss(search_term))
    for news in scraped_news:
        print(news)