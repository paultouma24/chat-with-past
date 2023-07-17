import streamlit as st
from ai import return_response
from chat import ChatBot

cb = ChatBot()

st.set_page_config("Journal Chat", page_icon="../favicon.png")
st.title("Chat with Your Past Journals")

prompt = st.text_input(
    "Prompt for your past journals",
)

if st.button("Ask"):
    if prompt != "":
        with st.spinner(text="In progress"):
            response = cb.get_response(prompt)
            st.text_area("Response", response, height=620)
