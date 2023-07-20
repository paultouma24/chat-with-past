from typing import List

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from util import debug, get_docs_from_fs

LOCAL_CHROMADB_DIR = "../local_chroma_db"
PRIVATE_JOURNALS_DIR = "../private-journals"
JOURNAL_DELIMETER = "| Journal Entry Separator |"


def get_client() -> chromadb.Client:
    client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory=LOCAL_CHROMADB_DIR)
    )
    return client


def get_journals_collection(client):
    journal_collection = client.get_or_create_collection("journal_entries")

    if journal_collection.count() == 0:
        first_time_journal_load(journal_collection)

    return journal_collection


def set_journal_path_in_db(client, path):
    collection = client.get_or_create_collection("journal_entries_path")
    collection.delete()
    collection.add(
        documents=[path],
        ids=["journal_entry_loc"],
    )


def get_journal_path_in_db(client):
    collection = client.get_or_create_collection("journal_entries_path")
    x = collection.peek()
    if not x["documents"]:
        return PRIVATE_JOURNALS_DIR
    else:
        return x["documents"][0]


def first_time_journal_load(collection):
    ids, documents = get_docs_from_fs(get_journal_path_in_db())
    if ids and documents:
        collection.add(ids=ids, documents=documents)


def n_nearest_neighbors(collection, prompt: str, n_results: int = 3) -> List[str]:
    basic_ef = embedding_functions.DefaultEmbeddingFunction()

    query_embeddings = basic_ef([prompt])

    documents = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_results,
    )["documents"][0]
    return JOURNAL_DELIMETER.join(documents)
