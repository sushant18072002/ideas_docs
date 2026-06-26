import urllib.request
import re
import sys
import time

pages = [
    '/gift-cards',
    '/coupons',
    '/max-coins',
    '/max-hotels',
    '/earn-max',
    '/blogs',
    '/terms-and-conditions',
    '/privacy-policy',
    '/refund-policy'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

base_url = 'https://www.maximize.money'

with open('maximize_pages.txt', 'w', encoding='utf-8') as out:
    for p in pages:
        url = base_url + p
        try:
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req).read().decode('utf-8')
            text = re.sub(r'<script.*?>.*?</script>', ' ', html, flags=re.DOTALL)
            text = re.sub(r'<style.*?>.*?</style>', ' ', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            out.write(f"==================== PAGE: {p} ====================\n")
            out.write(text[:3000] + "\n\n")
            print(f"Fetched {p}")
        except Exception as e:
            out.write(f"==================== PAGE: {p} (ERROR: {e}) ====================\n\n")
            print(f"Error {p}: {e}")
        time.sleep(0.5)

print("ALL PAGES SCRAPED")
