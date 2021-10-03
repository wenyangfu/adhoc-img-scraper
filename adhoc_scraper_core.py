import asyncio

from requests_html import HTMLSession

__headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
}

def fetch_image_urls(urls_file, fetch_page_image_urls):
    """
    fetch_page_image_urls should be a callback that handles image fetching for each URL in 'urls_file'.
    We assume a flow where we need to paginate through the user's feed and that relevant URLs are already present in the HTML.
    """
    urls = []
    with open(urls_file) as f:
        for url in f:
            urls.append(url)
    print(urls[0])
    print("------Synchronous step. Scrape all image URLs from webpages.--------")

    images = []
    session = HTMLSession()

    for url in urls:
        response = session.get(url, headers=__headers)
        page_img_urls = fetch_page_image_urls(response)

        images.extend(page_img_urls)

    print(f"Synchronous step done. {len(images)} images were found on urls given. Saving image urls to text file.")
    with open('images.txt', 'w') as f:
        for img_url in images:
            f.write(f"{img_url}\n")
    return images

async def download_image(url, session, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            filename = url.split('/')[-1]
            image = await response.read()
            print(f'Writing image {filename}')
            with open(f'images/{filename}', 'wb') as outfile:
                outfile.write(image)
            return filename

async def download_images(image_urls, session, semaphore):
    tasks = []

    for url in image_urls:
        task = asyncio.create_task(download_image(url, session, semaphore))
        tasks.append(task)

    return await asyncio.gather(*tasks)
