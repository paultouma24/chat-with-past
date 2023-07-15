import datetime
import os
from typing import List, Tuple

import chromadb
import docx
from chromadb.config import Settings
from chromadb.utils import embedding_functions

LOCAL_CHROMADB_DIR = "../local_chroma_db"
PRIVATE_JOURNALS_DIR = "../private-journals"
JOURNAL_DELIMETER = "A New Journal Entry: "


def debug(func):
    def wrapper(*args, **kwargs):
        # print the fucntion name and arguments
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        # call the function
        result = func(*args, **kwargs)
        # print the results
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


@debug
def get_client() -> chromadb.Client:
    client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory=LOCAL_CHROMADB_DIR)
    )
    return client


@debug
def get_collection(client):
    journal_collection = client.get_or_create_collection("journal_entries")

    if journal_collection.count() == 0:
        first_time_batch_load(journal_collection)

    return journal_collection


def remove_extension(file_name: str) -> str:
    name_without_extension = os.path.splitext(file_name)[0]
    return name_without_extension


def read_docx(file_path: str) -> str:
    document = docx.Document(file_path)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)


@debug
def get_info_from_fs(directory: str) -> Tuple[List[str], List[str], List[dict]]:
    documents = []
    metadatas = []
    ids = []
    count = 1
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            if file.startswith("."):
                continue

            # gather info from journals
            last_modified_date = str(
                datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            )
            title = remove_extension(file)
            text = read_docx(file_path)
            documents.append(f"{title} {text}")
            metadatas.append({"last_modified_date": last_modified_date})
            ids.append(f"Id{count}")
            count += 1

    return ids, documents, metadatas


@debug
def first_time_batch_load(collection):
    ids, documents, metadatas = get_info_from_fs(PRIVATE_JOURNALS_DIR)
    collection.add(ids=ids, documents=documents, metadatas=metadatas)


@debug
def n_nearest_neighbors(collection, prompt: str, n_results: int = 3) -> List[str]:
    basic_ef = embedding_functions.DefaultEmbeddingFunction()

    query_embeddings = basic_ef([prompt])

    documents = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_results,
    )["documents"][0]
    return JOURNAL_DELIMETER.join(documents)
