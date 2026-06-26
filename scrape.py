import urllib.request
import re
import sys

def fetch(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req).read().decode('utf-8')

html = fetch('https://www.maximize.money/')
links = set(re.findall(r'href=[\'"]([^\'"]+)[\'"]', html))

internal_links = []
for l in sorted(links):
    if l.startswith('/') or 'maximize.money' in l:
        internal_links.append(l)

text = re.sub(r'<script.*?>.*?</script>', ' ', html, flags=re.DOTALL)
text = re.sub(r'<style.*?>.*?</style>', ' ', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)

with open('maximize_summary.txt', 'w', encoding='utf-8') as f:
    f.write("=== LINKS ===\n")
    f.write("\n".join(internal_links) + "\n\n")
    f.write("=== HOMEPAGE TEXT ===\n")
    f.write(text)

print("SUCCESS")
