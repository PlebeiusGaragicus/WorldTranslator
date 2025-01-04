import os
import pathlib
from PIL import Image

import streamlit as st

from src.common import cprint, Colors
from src.rss import load_articles
from src.translator import translate_stream, translate
from src.reading import scrape_url, GROUND_TRUTH



STATIC_PATH = pathlib.Path(__file__).parent.parent / "static"

APP_NAME = "World News Translator"

# https://www.sozcu.com.tr/rss-servisleri


# https://www.sozcu.com.tr/feeds-rss-category-kripto


# COUNTIRES = ["🇺🇸 United States", "🇬🇧 United Kingdom", "🇩🇪 Germany", "🇪🇸 Spain", "🇹🇷 Turkey"]
COUNTIRES = ["🇹🇷 Turkey"]


def main_page():
    # ip_addr = st.context.headers.get('X-Forwarded-For', "?")
    # user_agent = st.context.headers.get('User-Agent', "?")
    # lang = st.context.headers.get('Accept-Language', "?")
    # cprint(f"RUNNING for: {ip_addr} - {lang} - {user_agent}", Colors.YELLOW)
    print(">>> RERUN")


    favicon = Image.open(os.path.join(STATIC_PATH, "favicon.ico"))
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.header("🗺️ :blue[World] :red[News]:green[Translator]", divider="rainbow")

    with st.popover("Choose a country" if st.session_state.get("country", None) == None else st.session_state.country):
        st.radio("Choose a country",
            options=COUNTIRES,
            index=None,
            horizontal=True,
            key="country",
            label_visibility="collapsed"
        )

    if st.session_state.get("country", None) is None:
        st.stop()




    if st.session_state.get("articles", None) == None:
        articles = load_articles("https://www.sozcu.com.tr/feeds-rss-category-kripto", max_articles=4)
        st.session_state.articles = articles



        def translate_article(article_url):
            article = next((a for a in st.session_state.articles if a['link'] == article_url), None)
            if article and "scraped" in article:
                with article_body_placeholders[article_url].container():
                    st.markdown("### :green[Translation]")
                    with st.spinner(":green[Translating...]"):
                        translation = translate(article["scraped"])
                        st.write(translation)

        article_body_placeholders = {}
        for article in st.session_state.articles:
                # article["title"] = translate(article["title"])
                # article["description"] = translate(article["description"])

            with st.container(border=True):
                with st.spinner(":green[Scraping...]"):
                    title = translate(article['title'])
                    st.markdown(f"### :blue[{title}]")

                    with st.popover("Origional content:", icon="📖"):
                        st.write(f"[Link to article]({article['link']})")
                        scraped = scrape_url( article['link'] )
                        st.markdown(scraped)
                        article["scraped"] = scraped

                article_body_placeholders[article['link']] = st.empty()
                article_body_placeholders[article['link']].button(
                    "Translate", 
                    on_click=translate_article, 
                    args=(article['link'],),
                    key=article['link']
                )


        # for article in st.session_state.articles:
        #     with article_body_placeholders.pop(0).container():
        #         st.markdown("### :green[Summary]")
        #         with st.spinner(":green[Translating summary...]"):
        #             st.write( translate_stream( article['description']) )

        #     st.markdown("### :green[Article]")
        #     with st.spinner(":green[Translating article...]"):
        #         st.write( translate_stream( article['scraped'] ) )



    if os.getenv("DEBUG"):
        with st.popover(":orange[DEBUG]"):
            st.write(st.session_state.articles)
            st.write(st.secrets)
            st.write( st.session_state )
            st.write( st.context.cookies )
            st.write( st.context.headers )
