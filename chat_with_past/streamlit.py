# import libraries

import streamlit as st
from chat import ChatBot
from db_util import get_current_path, load_new_folder_path

cb = ChatBot()

st.set_page_config("Journal Chat", page_icon="../favicon.png")
st.title("Chat with Your Past Journals")


current_journal_source = st.text(f"Current Journal Source: {get_current_path()}")

if st.button("Change Journal Source"):
    path = load_new_folder_path()
    if path:
        set_path_in_db()


prompt = st.text_input(
    "Prompt for your past journals",
)

if st.button("Ask"):
    if prompt != "":
        with st.spinner(text="In progress"):
            response = cb.get_response(prompt)
            st.text_area("Response", response, height=620)
