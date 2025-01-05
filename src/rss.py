import feedparser
from typing import List, Dict, Optional
import requests
from urllib.parse import urlparse


import streamlit as st

COUNTIRES = ["🇹🇷 Turkey", "🇩🇪 Germany", "🇪🇸 Spain"]

RSS_FEEDS = {
    "🇹🇷 Turkey": [
        {"Source": "Sozcu", "feed_name": "Economy", "url": "https://www.sozcu.com.tr/rss/ekonomi.xml"},
        {"Source": "Sozcu", "feed_name": "World", "url": "https://www.sozcu.com.tr/rss/dunya.xml"},
        {"Source": "Sozcu", "feed_name": "Technology", "url": "https://www.sozcu.com.tr/rss/teknoloji.xml"},
        {"Source": "Sozcu", "feed_name": "Sports", "url": "https://www.sozcu.com.tr/rss/spor.xml"},
        {"Source": "Hurriyet", "feed_name": "Main", "url": "https://www.hurriyet.com.tr/rss/anasayfa"},
        {"Source": "Hurriyet", "feed_name": "Economy", "url": "https://www.hurriyet.com.tr/rss/ekonomi"},
        {"Source": "Hurriyet", "feed_name": "World", "url": "https://www.hurriyet.com.tr/rss/dunya"},
        {"Source": "Hurriyet", "feed_name": "Technology", "url": "https://www.hurriyet.com.tr/rss/teknoloji"},
        {"Source": "Hurriyet", "feed_name": "Sports", "url": "https://www.hurriyet.com.tr/rss/spor"},
        {"Source": "Cumhuriyet", "feed_name": "Main", "url": "https://www.cumhuriyet.com.tr/rss/son_dakika.xml"},
        {"Source": "Cumhuriyet", "feed_name": "World", "url": "https://www.cumhuriyet.com.tr/rss/dunya"},
        {"Source": "Cumhuriyet", "feed_name": "Economy", "url": "https://www.cumhuriyet.com.tr/rss/ekonomi"},
        {"Source": "Cumhuriyet", "feed_name": "Politics", "url": "https://www.cumhuriyet.com.tr/rss/siyaset"},
        {"Source": "Der Spiegel", "feed_name": "Main", "url": "https://www.spiegel.de/schlagzeilen/tops/index.rss"},
    ],
    "🇩🇪 Germany": [
        {"Source": "Der Spiegel", "feed_name": "International", "url": "https://www.spiegel.de/ausland/index.rss"},
        {"Source": "Der Spiegel", "feed_name": "Politics", "url": "https://www.spiegel.de/politik/index.rss"},
        {"Source": "Der Spiegel", "feed_name": "Economy", "url": "https://www.spiegel.de/wirtschaft/index.rss"},
        {"Source": "Der Spiegel", "feed_name": "Science", "url": "https://www.spiegel.de/wissenschaft/index.rss"},
        {"Source": "FAZ", "feed_name": "Main", "url": "https://www.faz.net/rss/aktuell"},
        {"Source": "FAZ", "feed_name": "Politics", "url": "https://www.faz.net/rss/aktuell/politik"},
        {"Source": "FAZ", "feed_name": "Economy", "url": "https://www.faz.net/rss/aktuell/wirtschaft"},
        {"Source": "FAZ", "feed_name": "Finance", "url": "https://www.faz.net/rss/aktuell/finanzen"},
        {"Source": "FAZ", "feed_name": "Society", "url": "https://www.faz.net/rss/aktuell/gesellschaft"},
        {"Source": "Deutsche Welle", "feed_name": "Main", "url": "https://rss.dw.com/rdf/rss-de-all"},
        {"Source": "Deutsche Welle", "feed_name": "Germany", "url": "https://rss.dw.com/rdf/rss-de-ger"},
        {"Source": "Deutsche Welle", "feed_name": "Europe", "url": "https://rss.dw.com/rdf/rss-de-eu"},
        {"Source": "Deutsche Welle", "feed_name": "Business", "url": "https://rss.dw.com/rdf/rss-de-eco"},
        {"Source": "Deutsche Welle", "feed_name": "Culture", "url": "https://rss.dw.com/rdf/rss-de-cul"}
    ],
    "🇪🇸 Spain": [
        {"Source": "El País", "feed_name": "Main", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"},
        {"Source": "El País", "feed_name": "International", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada"},
        {"Source": "El País", "feed_name": "Economy", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/economia/portada"},
        {"Source": "El País", "feed_name": "Technology", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada"},
        {"Source": "El País", "feed_name": "Culture", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/cultura/portada"},
        {"Source": "El Mundo", "feed_name": "Main", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml"},
        {"Source": "El Mundo", "feed_name": "International", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml"},
        {"Source": "El Mundo", "feed_name": "Economy", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/economia.xml"},
        {"Source": "El Mundo", "feed_name": "Sports", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/deportes.xml"},
        {"Source": "El Mundo", "feed_name": "Culture", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/cultura.xml"},
        {"Source": "ABC", "feed_name": "Main", "url": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml"},
        {"Source": "ABC", "feed_name": "International", "url": "https://www.abc.es/rss/feeds/abc_Internacional.xml"},
        {"Source": "ABC", "feed_name": "Economy", "url": "https://www.abc.es/rss/feeds/abc_Economia.xml"},
        {"Source": "ABC", "feed_name": "Culture", "url": "https://www.abc.es/rss/feeds/abc_Cultura.xml"},
        {"Source": "ABC", "feed_name": "Science", "url": "https://www.abc.es/rss/feeds/abc_Ciencia.xml"}
    ]
}



@st.cache_data(ttl=3600)
def load_articles(feed_urls: List[str], max_articles: Optional[int] = None) -> List[Dict]:
    """
    Load articles from one or more RSS feeds.
    
    Args:
        feed_urls (List[str]): List of RSS feed URLs
        max_articles (Optional[int]): Maximum number of articles to return per feed. If None, returns all articles.
    
    Returns:
        List[Dict]: List of articles, each containing title, link, description, and published date
    """
    all_articles = []
    error_count = 0
    
    for feed_url in feed_urls:
        try:
            # First try to fetch the raw content with requests to handle encoding properly
            response = requests.get(feed_url, timeout=10)

            # Handle 404s with a subtle toast
            if response.status_code == 404:
                feed_name = next((source["Source"] + " - " + source["feed_name"] for source in RSS_FEEDS[st.session_state.country] if source["url"] == feed_url), feed_url)
                st.toast(f"`{feed_name}` is currently unavailable", icon="⚠️")
                continue

            # For other status codes, raise the error
            response.raise_for_status()
            
            # Try different encodings if needed
            try:
                content = response.content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    content = response.content.decode('iso-8859-1')
                except UnicodeDecodeError:
                    content = response.content.decode('utf-8', errors='ignore')
            
            feed = feedparser.parse(content)
            
            if feed.bozo and feed.bozo_exception:
                error_count += 1
                feed_name = next((source["Source"] + " - " + source["feed_name"] for source in RSS_FEEDS[st.session_state.country] if source["url"] == feed_url), feed_url)
                st.toast(f"⚠️ Error parsing {feed_name}", icon="⚠️")
                # Try parsing the URL directly as a fallback
                feed = feedparser.parse(feed_url)
            
            if not hasattr(feed, 'entries') or not feed.entries:
                continue
            
            entries = feed.entries[:max_articles] if max_articles else feed.entries

            # Get the base URL for resolving relative URLs
            parsed_url = urlparse(feed_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

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
                    'source': feed_url
                }
                all_articles.append(article)
                
        except requests.RequestException as e:
            error_count += 1
            feed_name = next((source["Source"] + " - " + source["feed_name"] for source in RSS_FEEDS[st.session_state.country] if source["url"] == feed_url), feed_url)
            if not (isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404):
                st.toast(f"🔴 Network error loading {feed_name}", icon="🔴")
            continue
        except Exception as e:
            error_count += 1
            feed_name = next((source["Source"] + " - " + source["feed_name"] for source in RSS_FEEDS[st.session_state.country] if source["url"] == feed_url), feed_url)
            st.toast(f"🔴 Error loading {feed_name}: {str(e)}", icon="🔴")
            continue
    
    # Show a summary toast if multiple errors occurred
    if error_count > 0:
        st.toast(f"⚠️ {error_count} feeds had errors. Some content may be missing.", icon="⚠️")
    
    return all_articles