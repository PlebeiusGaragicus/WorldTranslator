import os
import pathlib
from PIL import Image

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
        st.write(f"Selected {len(st.session_state.selected_sources)} feeds:")
        for source in st.session_state.selected_sources:
            st.write(f"- {source}")

        st.button(
            "Scrape Articles",
            help="Fetch articles from selected news sources",
            type="primary",
            use_container_width=True,
            on_click=do_the_thing,
            args=(article_placeholder,)
        )
    else:
        st.info("Please select at least one news feed")




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
def do_the_thing(article_placeholder):
    with article_placeholder.container():
        selected_country = st.session_state.country
        selected_sources = st.session_state.selected_sources
        feed_urls = [source["url"] for source in RSS_FEEDS[selected_country] if source["name"] in selected_sources]
        articles = load_articles(feed_urls, max_articles=st.session_state.max_articles)
        st.session_state.articles = articles

        # Display articles in a clean, organized way
        for article in st.session_state.articles:
            with st.container(border=True):
                # Translate and display the title
                with st.spinner(":green[Translating title...]"):
                    title = translate(article['title'])
                    st.markdown(f"### :blue[{title}]")

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
                    with st.spinner(":green[Translating summary...]"):
                        st.write(translate_stream(article['description']))
                    
                    if article.get("scraped"):
                        st.markdown("### :green[Article]")
                        with st.spinner(":green[Translating article...]"):
                            st.write(translate_stream(article['scraped']))



# def translate_article(article_url):
#     article = next((a for a in st.session_state.articles if a['link'] == article_url), None)
#     if article and "scraped" in article:
#         with article_body_placeholders[article_url].container():
#             st.markdown("### :green[Translation]")
#             with st.spinner(":green[Translating...]"):
#                 translation = translate(article["scraped"])
#                 st.write(translation)



# article_body_placeholders = {}
# for article in st.session_state.articles:

# ...

#         article_body_placeholders[article['link']] = st.empty()
#         article_body_placeholders[article['link']].button(
#             "Translate", 
#             on_click=translate_article, 
#             args=(article['link'],),
#             key=article['link']
#         )
