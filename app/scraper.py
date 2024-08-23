import aiohttp
from bs4 import BeautifulSoup
from app.cache import cache

# Scrape website content using aiohttp and BeautifulSoup libraries
# to extract text content from HTML pages asynchronously
async def scrape_website(url: str) -> str:
    # first check if the content is already in the cache
    cached_content = cache.get(url)
    if cached_content:
        return cached_content

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            # removed script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # get text content
            text = soup.get_text()

            # to break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())

            # to break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

            # to drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # store the content in the cache
            cache.set(url, text)

            return text


# example usage
if __name__ == "__main__":
    # by import asyncio here - scrape_website function can be used
    # in both synchronous and asynchronous contexts without modification.
    import asyncio

    # scrape a website
    url = "https://example.com"
    content = asyncio.run(scrape_website(url))
    print(content)
