from ai import load_ai, return_response
from db import (
    first_time_journal_load,
    get_client,
    get_journals_collection,
    n_nearest_neighbors,
)


class ChatBot:
    client = get_client()
    collection = get_journals_collection(client)

    def __init__(self):
        load_ai()

    def get_response(self, prompt):
        closest_docs = n_nearest_neighbors(self.collection, prompt)
        response = return_response(prompt, closest_docs)
        return response
