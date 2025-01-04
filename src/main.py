import os
import streamlit as st

from src.common import cprint, Colors
from src.interface import cmp_header, center_text

APP_NAME = "Template"


def log_rerun():
    ip_addr = st.context.headers.get('X-Forwarded-For', "?")
    user_agent = st.context.headers.get('User-Agent', "?")
    lang = st.context.headers.get('Accept-Language', "?")

    # print(f"RUNNING for IP address: {ip_addr}")
    cprint(f"RUNNING for: {ip_addr} - {lang} - {user_agent}", Colors.YELLOW)



def main_page():
    log_rerun()

    cmp_header(APP_NAME)

    center_text("p", "🗣️🤖💬", size=60) # or h1, whichever
    st.header("", divider="rainbow")

    st.write("Hello, Streamlit! 🎉")

    if os.getenv("DEBUG"):
        with st.sidebar:
            st.write(":orange[DEBUG]")
            st.write(st.secrets)
            st.write( st.session_state )
            st.write( st.context.cookies )
            st.write( st.context.headers )
