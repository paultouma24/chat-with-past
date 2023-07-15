from ai import load_ai, return_response
from db_util import debug, get_client, get_collection, n_nearest_neighbors


def run():
    client = get_client()
    collection = get_collection(client)
    load_ai()
    prompt = get_prompt()
    closest_docs = n_nearest_neighbors(collection, prompt)
    response = return_response(prompt, closest_docs)
    print(response)


@debug
def get_prompt():
    return "what would my past journals say about happiness?"


if __name__ == "__main__":
    run()
