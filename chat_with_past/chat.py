from ai import load_ai, return_response
from db_util import debug, get_client, get_collection, n_nearest_neighbors


class ChatBot:
    client = get_client()
    collection = get_collection(client)

    def __init__(self):
        load_ai()

    def get_response(self, prompt):
        closest_docs = n_nearest_neighbors(self.collection, prompt)
        response = return_response(prompt, closest_docs)
        return response
