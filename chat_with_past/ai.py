import os

import openai
from db_util import JOURNAL_DELIMETER
from dotenv import load_dotenv


# TODO: move to main method?
def load_ai():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    models = openai.Model.list()


def return_response(prompt, closest_docs):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""You are a kind and you are the the past self talking to the present self,
                  based on journal entries provided and separated by {JOURNAL_DELIMETER}) 
                  Be prophetic and cite examples in your responses from the journals.""",
            },
            {"role": "assistant", "content": closest_docs},
            {"role": "user", "content": prompt},
        ],
    )
    return response
