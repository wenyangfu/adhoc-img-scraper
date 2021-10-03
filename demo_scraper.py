import asyncio
import aiohttp
import requests

from adhoc_scraper_core import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
}


def image_fetcher(response):
    if  response.status_code == requests.codes.ok:
        img_elements = response.html.find('img.wbpic')
        img_urls = [img_element.attrs['src'] for img_element in img_elements
                        if 'src' in img_element.attrs]
        return [img_url.replace('bmiddle', 'large') for img_url in img_urls]


async def main():
    image_urls = fetch_image_urls('page_urls.txt', image_fetcher)

    print("Beginning async execution.")
    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(10) # 10 concurrent tasks maximum at any given time

    async with aiohttp.ClientSession(loop=loop, headers=headers) as session:
        task = asyncio.create_task(download_images(image_urls, session, semaphore))
        filenames = await task

if __name__ == "__main__":
    asyncio.run(main())