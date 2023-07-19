import os
import subprocess
from pathlib import Path
from typing import List, Tuple

import chromadb
import docx
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from llama_index import SimpleDirectoryReader

from helper import debug

LOCAL_CHROMADB_DIR = "../local_chroma_db"
PRIVATE_JOURNALS_DIR = "../private-journals"
JOURNAL_DELIMETER = "A New Journal Entry: "


def get_client() -> chromadb.Client:
    client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory=LOCAL_CHROMADB_DIR)
    )
    return client


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
def get_docs_from_fs(root: str) -> Tuple[List[str], List[str]]:
    documents = []
    ids = []

    subdirs = [
        os.path.join(root, dI)
        for dI in os.listdir(root)
        if os.path.isdir(os.path.join(root, dI))
    ]

    for dir in subdirs:
        loader = SimpleDirectoryReader(Path(dir))
        documents_ll = loader.load_data()

        documents.extend([documents.text for documents in documents_ll])
        ids.extend([documents.id_ for documents in documents_ll])

    return ids, documents


def get_current_path():
    return PRIVATE_JOURNALS_DIR


def load_new_folder_path():
    path = os.path.abspath("lib")
    p = subprocess.Popen(
        ["python3", "tkDirSelector.py"],
        cwd=path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result, error = p.communicate()
    p.terminate()
    ret_value = ""
    if isinstance(result, bytes):
        ret_value = result.decode("utf-8").strip()
    if isinstance(result, str):
        ret_value = result.strip()

    # check if ret_value is a valid path
    if os.path.isdir(ret_value):
        return ret_value
    return


def first_time_batch_load(collection):
    ids, documents = get_docs_from_fs(PRIVATE_JOURNALS_DIR)
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
