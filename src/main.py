import os
import pathlib
from PIL import Image
from datetime import datetime

import streamlit as st

from src.common import cprint, Colors
from src.rss import load_articles, RSS_FEEDS
from src.translator import translate_stream, translate
from src.reading import scrape_url


## VERSION TWO WILL HAVE A MAP WITH MARKERS FOR EACH COUNTRY WE HAVE AVAILABLE!!
# https://folium.streamlit.app/dynamic_updates




STATIC_PATH = pathlib.Path(__file__).parent.parent / "static"
APP_NAME = "World News Translator"

TARGET_LANGUAGE = "English"


# https://www.sozcu.com.tr/rss-servisleri
# 
# https://www.spiegel.de/dienste/besser-surfen-auf-spiegel-online-so-funktioniert-rss-a-1040321.html




def show_available_sources():
    """Display and handle the selection of news sources for the chosen country."""
    if not st.session_state.country:
        return

    available_sources = RSS_FEEDS[st.session_state.country]
    source_names = [source["name"] for source in available_sources]

    st.markdown("### :orange[News sources]")
    
    # Initialize selected_sources if not in session state
    if "selected_sources" not in st.session_state:
        st.session_state.selected_sources = []

    # Group sources by their main source (before the hyphen)
    source_groups = {}
    for name in source_names:
        main_source = name.split(" - ")[0]
        if main_source not in source_groups:
            source_groups[main_source] = []
        source_groups[main_source].append(name)

    # Create chunks of source groups for 3-column layout
    MAX_COLUMNS = 3
    source_groups_items = list(source_groups.items())
    num_groups = len(source_groups_items)
    
    # Calculate number of rows needed
    num_rows = (num_groups + MAX_COLUMNS - 1) // MAX_COLUMNS

    # Display sources in grid
    for row in range(num_rows):
        # Calculate number of columns for this row
        start_idx = row * MAX_COLUMNS
        end_idx = min(start_idx + MAX_COLUMNS, num_groups)
        current_row_items = source_groups_items[start_idx:end_idx]
        
        # Create columns for this row
        cols = st.columns(MAX_COLUMNS)
        
        # Display sources in this row
        for col_idx, (main_source, feeds) in enumerate(current_row_items):
            with cols[col_idx]:
                with st.container(border=True):
                    st.markdown(f"**{main_source}**")
                    for feed in feeds:
                        if st.checkbox(
                            feed.split(" - ")[1],  # Show only the feed type
                            value=feed in st.session_state.selected_sources,
                            key=f"source_checkbox_{feed}"
                        ):
                            if feed not in st.session_state.selected_sources:
                                st.session_state.selected_sources.append(feed)
                        else:
                            if feed in st.session_state.selected_sources:
                                st.session_state.selected_sources.remove(feed)




################################################################################################
def main_page():
    print(">>> RERUN")


    favicon = Image.open(os.path.join(STATIC_PATH, "favicon.ico"))
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Global storage for scraped articles
    if "all_scraped_articles" not in st.session_state:
        st.session_state.all_scraped_articles = {}  # {url: {"article": article_data, "timestamp": datetime, "source": source}}


    st.header("🗺️ :blue[World] :red[News]:green[Translator]", divider="rainbow")

    st.sidebar.slider(
        "Number of articles to display.",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        key="max_articles"
    )

    # with st.popover("Choose a country" if st.session_state.get("country", None) == None else st.session_state.country):
    st.segmented_control("Choose a country",
        options=RSS_FEEDS.keys(),
        default=None,
        key="country",
        # on_change=show_available_sources,
        label_visibility="collapsed"
    )

    show_available_sources()

    article_placeholder = st.empty()

    # Show selection summary and scrape button
    if st.session_state.get("selected_sources", None) and st.session_state.selected_sources:
    # if st.session_state.get("selected_sources", None):
        # st.write(f"Selected {len(st.session_state.selected_sources)} feeds:")
        # for source in st.session_state.selected_sources:
            # st.write(f"- {source}")

        st.button(
            "Scrape Articles",
            help="Fetch articles from selected news sources",
            type="primary",
            # use_container_width=True,
            on_click=scrape_articles,
            args=(article_placeholder,)
        )
    else:
        st.info("Please select at least one news feed")

    st.header("", divider="rainbow")


    # Show articles from memory and new scrapes
    show_articles()

    if os.getenv("DEBUG"):
        with st.popover(":orange[DEBUG]"):
            st.write("## articles")
            st.write(st.session_state.get("articles", None))
            st.divider()
            st.write(st.secrets)
            st.write( st.session_state )
            st.write( st.context.cookies )
            st.write( st.context.headers )
################################################################################################








################################################################################################
def scrape_articles(article_placeholder):
    with article_placeholder.container():
        selected_country = st.session_state.country
        selected_sources = st.session_state.selected_sources
        feed_urls = [source["url"] for source in RSS_FEEDS[selected_country] if source["name"] in selected_sources]
        
        # st.write("Debug - Selected sources:", selected_sources)
        # st.write("Debug - Feed URLs:", feed_urls)
        
        articles = load_articles(feed_urls, max_articles=st.session_state.max_articles)
        
        # Store articles in persistent storage with timestamp
        for article in articles:
            if article['link'] not in st.session_state.all_scraped_articles:
                # Find matching source name from the feed URL
                source_name = next(
                    (source["name"] for source in RSS_FEEDS[selected_country] 
                     if source["url"] == article.get("source")),  "Unknown Source"
                )

                st.session_state.all_scraped_articles[article['link']] = {
                    "article": article,
                    "timestamp": datetime.now(),
                    "source": source_name
                }

                st.write(f"Debug - Stored article with source: {source_name}")

def show_articles():
    # Filter articles based on selected sources
    selected_sources = st.session_state.get("selected_sources", [])
    
    if not st.session_state.all_scraped_articles:
        st.info("No articles have been scraped yet. Select sources and click 'Scrape Articles' to begin.")
        return
    # else:
        # st.write(f"Found {len(st.session_state.all_scraped_articles)} articles in memory.")
        # if selected_sources:
        #     st.write("Selected sources:", selected_sources)

    # Filter articles based on selected sources
    filtered_articles = {
        url: data for url, data in st.session_state.all_scraped_articles.items()
        if not selected_sources or data["source"] in selected_sources
    }

    if not filtered_articles:
        st.warning("No articles match the currently selected sources. Try selecting different sources or scraping new articles.")
        return

    # Group articles by country
    articles_by_country = {}
    for url, data in filtered_articles.items():
        # Find the matching country from RSS_FEEDS
        for country_key in RSS_FEEDS.keys():
            if any(source["name"] == data["source"] for source in RSS_FEEDS[country_key]):
                country = country_key
                break
        if country not in articles_by_country:
            articles_by_country[country] = []
        articles_by_country[country].append((url, data))

    # Create tabs for each country
    if articles_by_country:
        countries = sorted(articles_by_country.keys())
        # Create tabs with flags (flags are already included in the country keys)
        tabs = st.tabs(countries)

        # Display articles for each country in their respective tabs
        for country, tab in zip(countries, tabs):
            with tab:
                # st.markdown(f"## Articles from {country}")
                for url, data in articles_by_country[country]:
                    article = data["article"]
                    with st.container(border=True):
                        # Translate and display the title
                        with st.spinner(":green[Translating title...]"):
                            title = translate(article['title'])
                            st.markdown(f"### :blue[{title}]")
                            st.caption(f"Source: {data['source']} | Scraped: {data['timestamp']}")

                        # Show original content in a popover
                        with st.popover("Original content:", icon="📖"):
                            st.write(f"[Link to article]({article['link']})")
                            st.write("Original title:", article['title'])
                            st.write("Original description:", article['description'])

                        # Add a button to scrape and translate the full article
                        if st.button("Translate Full Article", key=f"translate_{article['link']}"):
                            with st.spinner(":green[Scraping article...]"):
                                scraped = scrape_url(article['link'])
                                article["scraped"] = scraped

                            st.markdown("### :green[Summary]")
                            if article.get("scraped"):
                                translate_stream(article["scraped"])
