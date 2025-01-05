import feedparser
from datetime import datetime
from collections import defaultdict

RSS_URLS = [
"https://www.cumhuriyet.com.tr/rss/son_dakika.xml",
"https://www.cumhuriyet.com.tr/rss/dunya",
"https://www.cumhuriyet.com.tr/rss/ekonomi",
"https://www.cumhuriyet.com.tr/rss/siyaset",
"https://www.hurriyet.com.tr/rss/spor",
]

def analyze_rss_feeds():
    url_count = defaultdict(list)
    
    for feed_url in RSS_URLS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:25]:  # Get top 15 articles
                url = entry.link
                url_count[url].append(feed_url)
        except Exception as e:
            print(f"Error processing {feed_url}: {str(e)}")
    
    # Analyze duplicates
    duplicates = {url: sources for url, sources in url_count.items() if len(sources) > 1}
    
    print(f"\nAnalysis completed at {datetime.now()}")
    print(f"Total unique URLs across all feeds: {len(url_count)}")
    print(f"Number of duplicate URLs: {len(duplicates)}")
    
    if duplicates:
        print("\nDuplicate URLs found in these feeds:")
        for url, sources in duplicates.items():
            print(f"\nURL: {url}")
            print("Found in feeds:")
            for source in sources:
                print(f"- {source}")

if __name__ == "__main__":
    analyze_rss_feeds()
