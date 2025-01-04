from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

import streamlit as st

MODEL = "llama3.1:latest"
OLLAMA_HOST = "http://host.docker.internal:11434"



INSTRUCTIONS = """


---

Translate the above into English.  Provide only ONE version of the translation.

Clean up formatting, if needed.  Ensure proper whitespace and punctuation.  Remove all markdown/rich text formatting.

Provide ONLY the cleaned and translated text - do not include any other information, cavets, warnings or explanations.
"""


@st.cache_data(ttl=3600)
def translate(text):
    stream = translate_stream(text)
    return ''.join(chunk.content for chunk in stream)


# @st.cache_data(ttl=3600)
def translate_stream(text):
    print(f"Translating: {text}")

    llm = ChatOllama(
        model=MODEL,
        keep_alive="5m",
        temperature=0.4,
        base_url=OLLAMA_HOST,
    )

    response = llm.stream([
        SystemMessage(content="You are a translator."),
        HumanMessage(content=f"{text}{INSTRUCTIONS}")
    ])

    # return response.content
    return response


# @st.cache_data(ttl=3600)
# def translate_and_summarize(text):
#     print(f"Summarizing: {text}")

#     llm = ChatOllama(
#         model=MODEL,
#         keep_alive="5m",
#         # temperature=0.7,
#         base_url=OLLAMA_HOST,
#     )

#     response = llm.invoke([
#         SystemMessage(content="You are a translator."),
#         HumanMessage(content=f"{text}\n\n---\n\nTranslate to English.  Provide ONLY the summary.  Clean up formatting, if needed.")
#     ])

#     return response.content