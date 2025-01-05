import os
import pathlib
from PIL import Image
from datetime import datetime

import streamlit as st


from src.rss import load_articles, RSS_FEEDS
from src.translator import translate_stream, translate
from src.reading import scrape_url


## VERSION TWO WILL HAVE A MAP WITH MARKERS FOR EACH COUNTRY WE HAVE AVAILABLE!!
# https://folium.streamlit.app/dynamic_updates




STATIC_PATH = pathlib.Path(__file__).parent.parent / "static"
APP_NAME = "World News Translator"

TARGET_LANGUAGE = "English"

INITIAL_VISIBLE_ARTICLES = 8
SHOW_MORE_BUTTON_COUNT = 4


# https://www.sozcu.com.tr/rss-servisleri
# 
# https://www.spiegel.de/dienste/besser-surfen-auf-spiegel-online-so-funktioniert-rss-a-1040321.html


################################################################################################
def main_page():
    print(">>> RERUN")


    favicon = Image.open(os.path.join(STATIC_PATH, "favicon.ico"))
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=favicon,
        # layout="wide",
        initial_sidebar_state="collapsed"
        # initial_sidebar_state="auto"
    )

    # Global storage for articles and selected sources
    if "articles" not in st.session_state:
        st.session_state.articles = {}
    
    if "articles_by_feed" not in st.session_state:
        st.session_state.articles_by_feed = {}
    
    if "selected_sources" not in st.session_state:
        st.session_state.selected_sources = {}

    if "selected_feed" not in st.session_state:
        st.session_state.selected_feed = None

    # st.markdown("### 🗣️🤷")
    st.header(":blue[World] :red[News] :green[Translator] 🗣️ 🤷 🌎", divider="rainbow")

    # Get unique countries from RSS_FEEDS
    countries = sorted(list(set(feed["country"] for feed in RSS_FEEDS)))

    # Create columns for countries (3 columns)
    cols = st.columns(3)

    # Display each country's feeds in a container
    for idx, country in enumerate(countries):
        with cols[idx % 3]:
            color = "grey"
            if st.session_state.selected_feed and st.session_state.selected_feed[0] == country:
                color = "orange"
            with st.expander(f":{color}[{country}]"):
                # st.subheader(country)

                # Group feeds by feed_name for this country
                country_feeds = [feed for feed in RSS_FEEDS if feed["country"] == country]
                sources = {}
                for feed in country_feeds:
                    feed_name = feed['feed_name']
                    if feed_name not in sources:
                        sources[feed_name] = []
                    sources[feed_name].append(feed)
                
                # Sort sources by number of feeds (largest first)
                sorted_sources = sorted(sources.items(), key=lambda x: len(x[1]), reverse=True)

                # Create vertical buttons for each feed
                for feed_name, feeds in sorted_sources:
                    if st.button(
                        # f"📰 {feed_name}",
                        f"{feed_name}",
                        key=f"btn_{country}_{feed_name}",
                        icon="🔴" if st.session_state.selected_feed == (country, feed_name) else "⭕️",
                        type="primary" if st.session_state.selected_feed == (country, feed_name) else "tertiary",
                        # use_container_width=True
                    ):
                        # Update global selection
                        st.session_state.selected_feed = (country, feed_name)
                        # Get the feed URL
                        feed_url = next(feed['url'] for feed in RSS_FEEDS 
                                    if feed['country'] == country and feed['feed_name'] == feed_name)
                        # Initialize articles for this feed if not exists
                        if feed_url not in st.session_state.articles_by_feed:
                            st.session_state.articles_by_feed[feed_url] = {}
                        # Update current articles to show this feed's articles
                        st.session_state.articles = st.session_state.articles_by_feed[feed_url]
                        st.rerun()


    # with st.popover(":grey[Settings]"):
    #     show_settings()

    # Update selected_sources based on selected_feed
    for country in st.session_state.selected_sources:
        st.session_state.selected_sources[country].clear()
    
    if st.session_state.selected_feed:
        country, feed_name = st.session_state.selected_feed
        if country not in st.session_state.selected_sources:
            st.session_state.selected_sources[country] = set()
        st.session_state.selected_sources[country].add(feed_name)

    with st.spinner("Displaying articles..."):
        show_articles()



    # # Show info message if no sources are selected
    # if not st.session_state.get("article_store", {}).get("selected_sources", []):
    #     st.info("Please select at least one source to view articles")



    if os.getenv("DEBUG"):
        # with st.popover(":orange[DEBUG]"):
        with st.sidebar:
            st.write("## articles")
            st.write(st.session_state.get("articles", None))
            st.divider()
            st.write(st.secrets)
            st.write( st.session_state )
            st.write( st.context.cookies )
            st.write( st.context.headers )
################################################################################################






def show_articles():
    """
    This displays the list of articles for the selected source.
    Articles are scraped and stored in memory when a source is selected.
    """
    
    # Get selected source using dictionary comprehension - more efficient than loop
    selected_sources = {
        country: next(iter(sources)) 
        for country, sources in st.session_state.selected_sources.items() 
        if sources
    }
    
    if not selected_sources:
        st.success("Select a news source.")
        return

    st.header(":rainbow[Articles]", divider="rainbow")
    
    # Get the first selected country and feed
    selected_country = next(iter(selected_sources.keys()))
    selected_feed = selected_sources[selected_country]
    
    # Create a feed lookup dictionary if not in session state
    if 'feed_lookup' not in st.session_state:
        st.session_state.feed_lookup = {
            (feed['country'], feed['feed_name']): feed['url']
            for feed in RSS_FEEDS
        }
    
    # Get feed URL using the lookup dictionary
    feed_url = st.session_state.feed_lookup.get((selected_country, selected_feed))
    if not feed_url:
        st.warning("No feed URL found for selected source")
        return
        
    # Initialize articles for this feed if not exists
    if feed_url not in st.session_state.articles_by_feed:
        st.session_state.articles_by_feed[feed_url] = {}
    
    # Set the current articles to this feed's articles
    st.session_state.articles = st.session_state.articles_by_feed[feed_url]
        
    # Initialize visible_count dictionary if not exists
    if 'visible_count_by_feed' not in st.session_state:
        st.session_state.visible_count_by_feed = {}
    
    # Initialize visible_count for this feed if not exists
    if feed_url not in st.session_state.visible_count_by_feed:
        st.session_state.visible_count_by_feed[feed_url] = INITIAL_VISIBLE_ARTICLES

    # Load new articles for selected source
    current_time = datetime.now()
    try:
        # new_articles = load_articles(feed_url, max_articles=st.session_state.get("max_articles", 5))
        # new_articles = load_articles(feed_url, max_articles=20)
        new_articles = load_articles(feed_url)
    except Exception as e:
        st.error(f"Failed to load articles: {str(e)}")
        return

    # Update articles dictionary with new articles
    for article in new_articles:
        article_url = article['link']
        
        # Skip if article is already in session state
        if article_url in st.session_state.articles:
            continue
            
        # Add new article with metadata
        article.update({
            'source': selected_feed,
            'scrape_time': current_time,
            'translated_title': None,
            'content': None,
            'translated': None,
            'visible': False  # Initially set to False
        })
        st.session_state.articles[article_url] = article
        # Also update the articles_by_feed dictionary
        st.session_state.articles_by_feed[feed_url][article_url] = article

    # Get all articles and sort by published date (newest first)
    all_articles = sorted(
        st.session_state.articles.items(),
        key=lambda x: x[1]['published'],
        reverse=True
    )

    # Mark the first N articles as visible
    for i, (article_url, article) in enumerate(all_articles):
        if i < st.session_state.visible_count_by_feed[feed_url]:
            article['visible'] = True

    # Display only visible articles
    for article_url, article in all_articles:
        if not article['visible']:
            continue

        with st.container(border=True):

            if article.get('translated_title', None) is None:
                with st.spinner(":green[Translating Title...]"):
                    article['translated_title'] = translate(article['title'])
            st.markdown(f"### :green[{article['translated_title']}]")

            st.caption(article.get('published', 'Unknown date'))

            # if article.get('translated_desc', None) is None:
            #     with st.spinner(":green[Translating Description...]"):
            #         article['translated_desc'] = st.write_stream(translate_stream(article['description']))
            # else:
            #     st.write(article['translated_desc'])

            with st.popover(":grey[Original Content]"):
                st.markdown(f"### [{article['title']}]({article_url})")
                st.caption(f":blue[Description:] {article.get('description', 'No description available')}")
                st.markdown("### :grey[Original Content]")

                # if we haven't scraped the content yet, scrape it
                if article.get('content', None) is None:
                    content = scrape_url(article_url)
                    article['content'] = content
                    article['translated'] = None

                st.caption(article['content'])

            translate_button(article, article_url)

    # Add "See more" button at the bottom if there are more articles to show
    # if len(all_articles) > st.session_state.visible_count_by_feed[feed_url]:
    #     if st.button("See more"):
    #         next_article_index = st.session_state.visible_count_by_feed[feed_url]
    #         all_articles[next_article_index][1]['visible'] = True
    #         st.session_state.visible_count_by_feed[feed_url] += 1
    #         st.rerun()

    # Add "See more" button at the bottom if there are more articles to show
    if len(all_articles) > st.session_state.visible_count_by_feed[feed_url]:
        st.button(":blue[Keep scrolling...]", icon="😉", use_container_width=True, type="tertiary", on_click=show_more, args=(feed_url,all_articles))
        # if st.button(":blue[Keep scrolling...]", icon="😉", use_container_width=True, type="tertiary", onclick=show_more):
            # with st.spinner("Loading..."):
            #     st.session_state.visible_count_by_feed[feed_url] += 3
            #     # Mark next batch of articles as visible
            #     for i, (article_url, article) in enumerate(all_articles):
            #         if i < st.session_state.visible_count_by_feed[feed_url]:
            #             article['visible'] = True
            # st.rerun()

def show_more(feed_url, all_articles):
    with st.spinner("Loading..."):
        st.session_state.visible_count_by_feed[feed_url] += SHOW_MORE_BUTTON_COUNT
        # Mark next batch of articles as visible
        for i, (article_url, article) in enumerate(all_articles):
            if i < st.session_state.visible_count_by_feed[feed_url]:
                article['visible'] = True



@st.fragment
def translate_button(article, article_url):
    if article['translated'] is None:
        # if st.session_state.get("auto_translate", False):
        #     with st.spinner(":green[Translating...]"):
        #         article['translated'] = st.write_stream(translate_stream(article['content']))

        # else:
        if st.button(":rainbow[Translate Article]", icon="🗣️", key=f"translate_{article['source']}{article_url}"):
            with st.spinner(":green[Translating...]"):
                article['translated'] = st.write_stream(translate_stream(article['content']))
                # st.rerun()

    else:
        # with st.container(border=True):
        st.markdown("### :orange[Translated Content]")
        st.write(article['translated'])
