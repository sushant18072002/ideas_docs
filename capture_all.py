import webbrowser
import time
import os
from PIL import ImageGrab

pages = [
    ('home', 'https://www.maximize.money/'),
    ('giftcards', 'https://www.maximize.money/gift-cards'),
    ('coupons', 'https://www.maximize.money/coupons'),
    ('maxcoins', 'https://www.maximize.money/max-coins'),
    ('maxhotels', 'https://www.maximize.money/max-hotels'),
    ('earnmax', 'https://www.maximize.money/earn-max')
]

print("Starting visual screen capture sequence across Chrome tabs...")

for name, url in pages:
    print(f"Opening {name} ({url})...")
    webbrowser.open(url)
    # Wait 5 seconds for Next.js hydration, Cloudflare pass, and animations
    time.sleep(5)
    shot_path = os.path.abspath(f'shot_{name}.png')
    img = ImageGrab.grab()
    img.save(shot_path)
    print(f"Captured {shot_path}")

print("SUCCESS: All visual screenshots captured.")
