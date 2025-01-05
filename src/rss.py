import feedparser
from typing import List, Dict, Optional
import requests
from urllib.parse import urlparse

import streamlit as st


RSS_FEEDS = [
    {"country": "🇹🇷 Turkey", "feed_name": "Sozcu - Economy", "url": "https://www.sozcu.com.tr/rss/ekonomi.xml"},
    {"country": "🇹🇷 Turkey", "feed_name": "Hurriyet - Main", "url": "https://www.hurriyet.com.tr/rss/anasayfa"},
    {"country": "🇹🇷 Turkey", "feed_name": "Cumhuriyet - Main", "url": "https://www.cumhuriyet.com.tr/rss/son_dakika.xml"},
    {"country": "🇪🇸 Spain", "feed_name": "El País - Main", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"},
    {"country": "🇪🇸 Spain", "feed_name": "El Mundo - Main", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml"},
    {"country": "🇪🇸 Spain", "feed_name": "ABC - Main", "url": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml"},
]


@st.cache_data(ttl=3600)
def load_articles(feed_url: str, max_articles: Optional[int] = None) -> List[Dict]:
    """
    Load articles from a single RSS feed.
    
    Args:
        feed_url (str): RSS feed URL
        max_articles (Optional[int]): Maximum number of articles to return. If None, returns all articles.
    
    Returns:
        List[Dict]: List of articles, each containing title, link, description, and published date
        
    Raises:
        requests.exceptions.RequestException: If there's an error fetching the feed
        Exception: For other unexpected errors
    """
    # Fetch the feed content
    response = requests.get(feed_url, timeout=10)
    response.raise_for_status()
    
    # Parse the feed
    feed = feedparser.parse(response.content)
    
    if not hasattr(feed, 'entries') or not feed.entries:
        return []
    
    # Get the base URL for resolving relative URLs
    parsed_url = urlparse(feed_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Process entries
    articles = []
    entries = feed.entries[:max_articles] if max_articles else feed.entries
    
    for entry in entries:
        # Handle relative URLs in links
        link = entry.get('link', '')
        if link and not link.startswith(('http://', 'https://')):
            link = base_url + link if link.startswith('/') else base_url + '/' + link

        article = {
            'title': entry.get('title', ''),
            'link': link,
            'description': entry.get('description', ''),
            'published': entry.get('published', ''),
            'author': entry.get('author', 'Unknown'),
            'feed_url': feed_url
        }
        articles.append(article)
        
    return articles