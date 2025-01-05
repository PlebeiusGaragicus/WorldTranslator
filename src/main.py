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

    # Global storage for scraped articles
    if "article_store" not in st.session_state:
        # st.session_state.article_store = {}

        # Create an empty dictioinary based on RSS_FEEDS keys
        st.session_state.article_store = {key: {} for key in RSS_FEEDS.keys()}


    st.header("🗺️ :blue[World] :orange[-] :red[News] :orange[-] :green[Translator]", divider="rainbow")


    # with st.popover("Choose a country" if st.session_state.get("country", None) == None else st.session_state.country):
    st.segmented_control("Choose a country",
        options=RSS_FEEDS.keys(),
        default=None,
        key="country",
        label_visibility="collapsed"
    )

    # with st.popover(":red[Settings]", icon=":material/settings:"):
    with st.sidebar:
        st.header(":orange[:material/settings:] :red[Settings]", divider="rainbow")
        show_settings()


    show_available_sources()

    show_articles()



    # # Show info message if no sources are selected
    # if not st.session_state.get("article_store", {}).get("selected_sources", []):
    #     st.info("Please select at least one source to view articles")



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
# def scrape_articles(article_placeholder):
#     with article_placeholder.container():
#         selected_country = st.session_state.country
#         selected_sources = st.session_state.selected_sources
#         feed_urls = [source["url"] for source in RSS_FEEDS[selected_country] if source["name"] in selected_sources]
    
        
#         articles = load_articles(feed_urls, max_articles=st.session_state.max_articles)
        
#         # Store articles in persistent storage with timestamp
#         for article in articles:
#             if article['link'] not in st.session_state.all_scraped_articles:
#                 # Find matching source name from the feed URL
#                 source_name = next(
#                     (source["name"] for source in RSS_FEEDS[selected_country] 
#                      if source["url"] == article.get("source")),  "Unknown Source"
#                 )

#                 st.session_state.all_scraped_articles[article['link']] = {
#                     "article": article,
#                     "timestamp": datetime.now(),
#                     "source": source_name
#                 }


def show_available_sources():
    """
    This displays the available sources for the currently selected country and manages their selection state.
    The function updates the article_store in session state to maintain selected source states and their articles.
    Articles from unselected sources are retained in memory but not displayed.
    Sources are displayed in a grid with exactly 3 columns per row, each taking 1/3rd of the width.
    Source groups are sorted by number of feeds, with largest groups first.
    """
    if not st.session_state.country:
        return

    available_sources = RSS_FEEDS[st.session_state.country]
    
    # Initialize article store for current country if not exists
    if st.session_state.country not in st.session_state.article_store:
        st.session_state.article_store[st.session_state.country] = {}
    
    # Group sources by their main source name
    source_groups = {}
    for source in available_sources:
        main_source = source["Source"]  # Use "Source" instead of "name"
        if main_source not in source_groups:
            source_groups[main_source] = []
        source_groups[main_source].append(source)
    
    # Sort sources by number of feeds (descending) and then alphabetically for ties
    sorted_sources = sorted(
        source_groups.keys(),
        key=lambda x: (-len(source_groups[x]), x)
    )
    
    # Calculate number of rows needed (always 3 columns per row)
    MAX_COLS = 3
    num_sources = len(sorted_sources)
    num_rows = (num_sources + MAX_COLS - 1) // MAX_COLS
    
    # Display sources in a grid, always 3 columns per row
    for row in range(num_rows):
        start_idx = row * MAX_COLS
        end_idx = min(start_idx + MAX_COLS, num_sources)
        row_sources = sorted_sources[start_idx:end_idx]

        # Always create 3 columns for consistent width
        cols = st.columns(3)
        
        # Display sources in their respective columns
        for col_idx, main_source in enumerate(row_sources):
            with cols[col_idx]:
                
                # Create a container with a border for the source's feeds
                with st.container(border=True):
                    st.markdown(f"### :orange[{main_source}]")
                    for feed in sorted(source_groups[main_source], key=lambda x: x['feed_name']):
                        display_name = f"{feed['Source']} - {feed['feed_name']}"
                        
                        # Initialize source in article store if not exists
                        if display_name not in st.session_state.article_store[st.session_state.country]:
                            st.session_state.article_store[st.session_state.country][display_name] = {
                                "selected": False,
                                "articles": [],
                                # always use the current time!
                                "last_updated": datetime.now()
                            }
                        
                        # Create checkbox for source selection, showing only the feed name
                        source_selected = st.checkbox(
                            feed['feed_name'],  # Show only the feed type, since we have the source name as header
                            value=st.session_state.article_store[st.session_state.country][display_name]["selected"],
                            key=f"source_{st.session_state.country}_{display_name}"
                        )
                        
                        # Update selection state in article store
                        st.session_state.article_store[st.session_state.country][display_name]["selected"] = source_selected


def show_settings():
    # auto-translate toggle
    st.toggle(
        ":blue[Auto-Translate]",
        key="auto_translate"
    )

    # Number of articles to scrape per source
    st.slider(
        ":red[Number of articles to scrape per source]",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        key="max_articles"
    )


def show_articles():
    """
    This displays the list of articles for each selected source in their own tabs.
    Articles are scraped and stored in memory when sources are selected.
    Each source's articles are displayed in their own tab.
    """
    
    if not st.session_state.get("country"):
        st.success("Select a country.")
        return
    


    selected_country = st.session_state.country
    country_store = st.session_state.article_store.get(selected_country, {})
    
    # Get selected sources from article_store
    selected_sources = [
        source_name for source_name, source_data in country_store.items()
        if source_data.get("selected", False)
    ]


    if not selected_sources:
        st.success("Select a news source.")
        return

    st.header(":rainbow[Articles]", divider="rainbow")

    
    # Get feed URLs for selected sources
    feed_urls = []
    source_url_map = {}  # Maps URLs back to source names
    for source in RSS_FEEDS[selected_country]:
        display_name = f"{source['Source']} - {source['feed_name']}"
        if display_name in selected_sources:
            feed_urls.append(source["url"])
            source_url_map[source["url"]] = display_name
    
    if not feed_urls:
        st.warning("No feed URLs found for selected sources")
        return
        
    # Load new articles for selected sources
    current_time = datetime.now() # always use the current time!
    new_articles = load_articles(feed_urls, max_articles=st.session_state.get("max_articles", 10))

    # unique_articles = []
    # existing_links = []
    # for country in st.session_state.article_store:
    #     for source in st.session_state.article_store[country]:
    #         for article in st.session_state.article_store[country][source]['articles']:
    #             existing_links.append(article['link'])

    # st.write(existing_links)

    # unique = []
    # for article in new_articles:
    #     if article["link"] not in existing_links:
    #         # new_articles.remove(article)
    #         unique.append(article)


    # st.write(unique)

    #             # if article['link'] in new_links:
    #             #     # new_articles.remove(article['link'])
    #             #     unique_articles.add(article)
    #             #     st.toast("removed duplicate")
# f"translate_{article['link']}"
    unique_articles = [article for article in new_articles if f"translate_{article['link']}" not in st.session_state]



    # Update article store with new articles
    for article in unique_articles:
        if st.session_state.get(f"translate_{article['link']}", None) is not None:
            continue

        article_key = article['link']
        # The feed URL is stored in the 'source' field of the article
        source_name = source_url_map.get(article.get('source'))
        
        if not source_name:
            st.warning(f"Could not map article to source. Article source: {article.get('source')}")
            continue

        # Add article to source's article list if not already present
        source_articles = country_store[source_name]["articles"]
        if not any(existing['link'] == article_key for existing in source_articles):
            article['source'] = source_name
            article['scrape_time'] = current_time
            source_articles.append(article)
            country_store[source_name]["last_updated"] = current_time.isoformat()

    # Create tabs for each selected source
    if selected_sources:
        tabs = st.tabs(selected_sources)
        
        # Display articles for each source in its tab
        for tab, source_name in zip(tabs, selected_sources):
            with tab:
                source_data = country_store[source_name]
                source_articles = source_data["articles"]
                
                if not source_articles:
                    st.info(f"No articles found for {source_name}")
                    continue

                # Sort articles by published date (newest first)
                source_articles.sort(key=lambda x: x.get('published', ''), reverse=True)

                # Display articles
                for article in source_articles:
                    # check if this key already exists: f"translate_{article['link']}"

                    with st.container(border=True):
                        # if st.session_state.get(f"translate_{article['link']}", None) is not None:
                        #     st.warning("Skipping duplicate article")
                        #     continue

                        st.markdown(f"### [{article['title']}]({article['link']})")

                        if article.get('translated_title', None) is None:
                            with st.spinner(":green[Translating Title...]"):
                                article['translated_title'] = translate(article['title'])
                        # st.write(article['translated_title'])
                        st.markdown(f"### :green[{article['translated_title']}]")

                        st.caption(article.get('published', 'Unknown date'))
                        st.caption(f":blue[Description:] {article.get('description', 'No description available')}")

                        if article.get('translated_desc', None) is None:
                            # article['translated_desc'] = translate(article['description'])
                            with st.spinner(":green[Translating Description...]"):
                                article['translated_desc'] = st.write_stream( translate_stream(article['description']) )
                        else:
                            st.write(article['translated_desc'])

                        # st.markdown(f"### {article['title']}")
                        # st.caption(f":red[Title:] {article.get('title', 'No description available')}")

                        


                        with st.popover(":grey[Original Content]"):
                            st.markdown("### :grey[Original Content]")

                            # if we haven't scraped the content yet, scrape it
                            if article.get('content', None) is None:
                                content = scrape_url(article['link'])
                                article['content'] = content
                                article['translated'] = None

                            st.caption(article['content'])

                        if article['translated'] is None:
                            if st.session_state.auto_translate:
                                with st.spinner(":green[Translating...]"):
                                    article['translated'] = st.write_stream( translate_stream(article['content']) )
                                    # st.rerun()

                            else:
                                if st.button(":rainbow[Translate Article]", icon="🗣️", key=f"translate_{article['source']}{article['link']}"):
                                # if st.button(":rainbow[Translate Article]", icon="🗣️"):
                                    with st.spinner(":green[Translating...]"):
                                        article['translated'] = st.write_stream( translate_stream(article['content']) )
                                        st.rerun()

                        else:
                            with st.container(border=True):
                                st.markdown("### :green[Translated Content]")
                                st.write(article['translated'])
