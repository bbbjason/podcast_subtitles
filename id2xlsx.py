# Description: Obtain the RSS feed URL from a provided Apple Podcast ID (via command line) and record podcast entries from the RSS feed into an Excel file
import sys
import requests
import feedparser
from datetime import datetime
import openpyxl

# --- Command line Apple Podcast ID input ---
if len(sys.argv) < 2:
    print("Usage: python id2xlsx.py <apple_podcast_id>")
    exit(1)
apple_podcast_id = sys.argv[1]

# --- ID lookup part ---
lookup_url = f'https://itunes.apple.com/lookup?id={apple_podcast_id}'
response = requests.get(lookup_url)
data = response.json()

if data.get('resultCount', 0) > 0:
    feed_url = data['results'][0]['feedUrl']
else:
    print('Cannot find the podcast by the Apple Podcast ID.')
    exit(1)

# --- RSS feed parsing and Excel recording part ---
try:
    feed = feedparser.parse(feed_url)    
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["title", "published", "audio_url"])
    
    for entry in feed.entries:
        title = entry.title
        published = entry.get("published", "N/A")
        if published != "N/A":
            try:
                dt = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %Z')
                published = f"{dt.year:04d}_{dt.month:02d}_{dt.day:02d}_{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}"
            except Exception as e:
                published = published.replace(',', '').replace(' ', '_')
        audio_url = entry.enclosures[0]['href'] if entry.enclosures else "N/A"
        ws.append([title, published, audio_url])
    
    wb.save('podcast_entries.xlsx')
    print("Excel file 'podcast_entries.xlsx' saved.")
    
except Exception as e:
    print(f"Program execution error: {e}")