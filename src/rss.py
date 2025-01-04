import feedparser
from typing import List, Dict, Optional


import streamlit as st


@st.cache_data(ttl=3600)
def load_articles(feed_url: str, max_articles: Optional[int] = None) -> List[Dict]:
    """
    Load articles from an RSS feed.
    
    Args:
        feed_url (str): URL of the RSS feed
        max_articles (Optional[int]): Maximum number of articles to return. If None, returns all articles.
    
    Returns:
        List[Dict]: List of articles, each containing title, link, description, and published date
    """

    print(f"Loading RSS feed: {feed_url}")
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:  # feedparser sets bozo to 1 if there was a problem parsing the feed
            print(f"Error parsing feed: {feed.bozo_exception}")
            return []
        
        articles = []
        entries = feed.entries[:max_articles] if max_articles else feed.entries
        
        for entry in entries:
            article = {
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'description': entry.get('description', ''),
                'published': entry.get('published', ''),
                'author': entry.get('author', 'Unknown')
            }
            articles.append(article)
            
        return articles
        
    except Exception as e:
        logging.error(f"Error loading RSS feed: {str(e)}")
        return []