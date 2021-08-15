import argparse
import asyncio
import json
from urllib import parse as urlparse

from playwright.async_api import async_playwright

KEYWORDS = [
    'facebook ads',
    'local facebook ads',
    'small business facebook ads',
    'online facebook ads',
    'buy facebook ads',
    'facebook advertising'
]


parser = argparse.ArgumentParser(description='Scrape gclid from google ads')
parser.add_argument('-k', '--keywords', action='append', required=True)

async def main():
    keywords = parser.parse_args().keywords
    async with async_playwright() as p:
        browser = await p.webkit.launch()
        page = await browser.new_page()
        for keyword in keywords:
            await page.goto('https://google.com/search?q=' + urlparse.quote(keyword))
            await page.wait_for_load_state()
            num_ads = await page.locator('div[aria-label="Ads"] a:not([href*="https://www.google.com"])').count()
            gclid = None
            if num_ads > 0:
                await page.click('div[aria-label="Ads"] a:not([href*="https://www.google.com"])')
                await asyncio.sleep(3)
                await page.wait_for_load_state()
                parsed = urlparse.parse_qs(page.url)
                gclid = parsed.get('gclid', [None])[0]
            print(json.dumps({'keyword': keyword, 'gclid': gclid}))
        await browser.close()

asyncio.run(main())