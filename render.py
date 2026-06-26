import webbrowser
import time
import os
import subprocess
import re
import sys

pages = [
    '/',
    '/gift-cards',
    '/coupons',
    '/max-coins',
    '/max-hotels',
    '/earn-max',
    '/blogs'
]
base_url = 'https://www.maximize.money'

print("1. Opening browser tabs on user screen...")
for p in pages:
    webbrowser.open(base_url + p)
    time.sleep(0.3)

print("2. Locating Chrome or Edge binary for full DOM rendering...")
candidates = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe")
]

browser_exe = None
for c in candidates:
    if os.path.exists(c):
        browser_exe = c
        break

if not browser_exe:
    print("Could not find browser binary.")
    sys.exit(0)

print(f"Found browser binary: {browser_exe}")

with open('maximize_pages_rendered.txt', 'w', encoding='utf-8') as out:
    for p in pages:
        url = base_url + p
        print(f"Rendering DOM for {p}...")
        try:
            cmd = [
                browser_exe,
                '--headless=new',
                '--disable-gpu',
                '--dump-dom',
                '--virtual-time-budget=5000',
                url
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore', timeout=20)
            html = res.stdout
            text = re.sub(r'<script.*?>.*?</script>', ' ', html, flags=re.DOTALL)
            text = re.sub(r'<style.*?>.*?</style>', ' ', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            out.write(f"==================== RENDERED PAGE: {p} ====================\n")
            out.write(text[:5000] + "\n\n")
        except Exception as e:
            out.write(f"==================== RENDERED PAGE: {p} (ERROR: {e}) ====================\n\n")

print("SUCCESS: DOM rendered.")
