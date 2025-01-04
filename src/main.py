import os
import pathlib
from PIL import Image

import streamlit as st

from src.common import cprint, Colors
from src.rss import load_articles
from src.translator import translate_stream, translate
from src.reading import scrape_url


STATIC_PATH = pathlib.Path(__file__).parent.parent / "static"
APP_NAME = "World News Translator"



COUNTIRES = ["🇹🇷 Turkey", "🇩🇪 Germany", "🇪🇸 Spain"]


# https://www.sozcu.com.tr/rss-servisleri
# https://www.sozcu.com.tr/feeds-rss-category-kripto
# https://www.spiegel.de/dienste/besser-surfen-auf-spiegel-online-so-funktioniert-rss-a-1040321.html
RSS_FEEDS = {
    # "🇺🇸 United States": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    # "🇬🇧 United Kingdom": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "🇹🇷 Turkey": "https://www.sozcu.com.tr/feeds-rss-category-kripto",
    "🇩🇪 Germany": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
    "🇪🇸 Spain": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"
}





################################################################################################
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

    st.sidebar.slider(
        "Number of articles to display.",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        key="max_articles"
    )

    with st.popover("Choose a country" if st.session_state.get("country", None) == None else st.session_state.country):
        st.radio("Choose a country",
            options=COUNTIRES,
            index=None,
            horizontal=True,
            key="country",
            on_change=main_page,
            label_visibility="collapsed"
        )

    if st.session_state.country:
        do_the_thing()





################################################################################################
def do_the_thing():
    selected_country = st.session_state.country
    feed_url = RSS_FEEDS[selected_country]
    articles = load_articles(feed_url, max_articles=st.session_state.max_articles)
    st.session_state.articles = articles
    st.popover("Articles:", icon="📖").write(st.session_state.articles)



    # This will hold the article body placeholders, that will be translated AFTER each article's title is displayed
    article_body_placeholders = []

    # First we translate and display the titles for each article
    for article in st.session_state.articles:
        with st.container(border=True):
            with st.spinner(":green[Scraping...]"):
                title = translate(article['title'])
                st.markdown(f"### :blue[{title}]")

                with st.popover("Origional content:", icon="📖"):
                    st.write(f"[Link to article]({article['link']})")
                    scraped = scrape_url( article['link'] )
                    st.markdown(scraped)
                    article["scraped"] = scraped

            article_body_placeholders.append( st.empty() )


    # Now we translate and display the bodies for each article
    for article in st.session_state.articles:

        with article_body_placeholders.pop(0).container():
            # skip_button = st.empty()

            # if skip_button.button("Skip", on_click=main_page, key=article['link']):
            #     skip_button.empty()
            #     continue

            st.markdown("### :green[Summary]")
            with st.spinner(":green[Translating summary...]"):
                st.write( translate_stream( article['description']) )
            
            st.markdown("### :green[Article]")
            with st.spinner(":green[Translating article...]"):
                st.write( translate_stream( article['scraped'] ) )




    if os.getenv("DEBUG"):
        with st.popover(":orange[DEBUG]"):
            st.write(st.session_state.articles)
            st.write(st.secrets)
            st.write( st.session_state )
            st.write( st.context.cookies )
            st.write( st.context.headers )







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
