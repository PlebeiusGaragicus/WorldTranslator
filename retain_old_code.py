"""
This file contains the old version of RSS_FEEDS before refactoring the structure.
Saved at: 2025-01-04T15:24:39-08:00
"""

RSS_FEEDS = {
    "🇹🇷 Turkey": [
        {"name": "Hurriyet - Main", "url": "https://www.hurriyet.com.tr/rss/anasayfa"},
        {"name": "Sozcu - Economy broken", "url": "https://www.sozcu.com.tr/rss/ekonomi.xml"},
        {"name": "Sozcu - World broken", "url": "https://www.sozcu.com.tr/rss/dunya.xml"},
        {"name": "Sozcu - Technology broken", "url": "https://www.sozcu.com.tr/rss/teknoloji.xml"},
        {"name": "Sozcu - Sports broken", "url": "https://www.sozcu.com.tr/rss/spor.xml"},
        {"name": "Hurriyet - Economy", "url": "https://www.hurriyet.com.tr/rss/ekonomi"},
        {"name": "Hurriyet - World", "url": "https://www.hurriyet.com.tr/rss/dunya"},
        {"name": "Hurriyet - Technology", "url": "https://www.hurriyet.com.tr/rss/teknoloji"},
        {"name": "Hurriyet - Sports", "url": "https://www.hurriyet.com.tr/rss/spor"},
        {"name": "Cumhuriyet - Main", "url": "https://www.cumhuriyet.com.tr/rss/son_dakika.xml"},
        {"name": "Cumhuriyet - World", "url": "https://www.cumhuriyet.com.tr/rss/dunya"},
        {"name": "Cumhuriyet - Economy", "url": "https://www.cumhuriyet.com.tr/rss/ekonomi"},
        {"name": "Cumhuriyet - Politics", "url": "https://www.cumhuriyet.com.tr/rss/siyaset"},
        {"name": "Der Spiegel - Main", "url": "https://www.spiegel.de/schlagzeilen/tops/index.rss"}
    ],
    "🇩🇪 Germany": [
        {"name": "Der Spiegel - Main", "url": "https://www.spiegel.de/schlagzeilen/tops/index.rss"},
        {"name": "Der Spiegel - International", "url": "https://www.spiegel.de/ausland/index.rss"},
        {"name": "Der Spiegel - Politics", "url": "https://www.spiegel.de/politik/index.rss"},
        {"name": "Der Spiegel - Economy", "url": "https://www.spiegel.de/wirtschaft/index.rss"},
        {"name": "Der Spiegel - Science", "url": "https://www.spiegel.de/wissenschaft/index.rss"},
        {"name": "FAZ - Main", "url": "https://www.faz.net/rss/aktuell"},
        {"name": "FAZ - Politics", "url": "https://www.faz.net/rss/aktuell/politik"},
        {"name": "FAZ - Economy", "url": "https://www.faz.net/rss/aktuell/wirtschaft"},
        {"name": "FAZ - Finance", "url": "https://www.faz.net/rss/aktuell/finanzen"},
        {"name": "FAZ - Society", "url": "https://www.faz.net/rss/aktuell/gesellschaft"},
        {"name": "Deutsche Welle - Main", "url": "https://rss.dw.com/rdf/rss-de-all"},
        {"name": "Deutsche Welle - Germany", "url": "https://rss.dw.com/rdf/rss-de-ger"},
        {"name": "Deutsche Welle - Europe", "url": "https://rss.dw.com/rdf/rss-de-eu"},
        {"name": "Deutsche Welle - Business", "url": "https://rss.dw.com/rdf/rss-de-eco"},
        {"name": "Deutsche Welle - Culture", "url": "https://rss.dw.com/rdf/rss-de-cul"}
    ],
    "🇪🇸 Spain": [
        {"name": "El País - Main", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"},
        {"name": "El País - International", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada"},
        {"name": "El País - Economy", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/economia/portada"},
        {"name": "El País - Technology", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada"},
        {"name": "El País - Culture", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/cultura/portada"},
        {"name": "El Mundo - Main", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml"},
        {"name": "El Mundo - International", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml"},
        {"name": "El Mundo - Economy", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/economia.xml"},
        {"name": "El Mundo - Sports", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/deportes.xml"},
        {"name": "El Mundo - Culture", "url": "https://e00-elmundo.uecdn.es/elmundo/rss/cultura.xml"},
        {"name": "ABC - Main", "url": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml"},
        {"name": "ABC - International", "url": "https://www.abc.es/rss/feeds/abc_Internacional.xml"},
        {"name": "ABC - Economy", "url": "https://www.abc.es/rss/feeds/abc_Economia.xml"},
        {"name": "ABC - Culture", "url": "https://www.abc.es/rss/feeds/abc_Cultura.xml"},
        {"name": "ABC - Science", "url": "https://www.abc.es/rss/feeds/abc_Ciencia.xml"}
    ]
}

## OLD VERSION
def show_available_sources():
    """Display and handle the selection of news sources for the chosen country."""

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
                            key=f"source_checkbox_{feed}",
                        ):
                            if feed not in st.session_state.selected_sources:
                                st.session_state.selected_sources.append(feed)
                        else:
                            if feed in st.session_state.selected_sources:
                                st.session_state.selected_sources.remove(feed)
