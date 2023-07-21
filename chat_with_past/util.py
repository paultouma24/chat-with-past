import os
import subprocess
from pathlib import Path
from typing import List, Tuple

from llama_index import SimpleDirectoryReader


def debug(func):
    def wrapper(*args, **kwargs):
        # print the function name and arguments
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        # call the function
        result = func(*args, **kwargs)
        # print the results
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


@debug
def get_docs_from_fs(root: str) -> Tuple[List[str], List[str]]:
    documents = []
    ids = []

    subdirs = [
        os.path.join(root, dI)
        for dI in os.listdir(root)
        if os.path.isdir(os.path.join(root, dI)) and not dI.startswith(".")
    ]

    for dir in subdirs:
        loader = SimpleDirectoryReader(Path(dir))
        documents_ll = loader.load_data()

        documents.extend([documents.text for documents in documents_ll])
        ids.extend([documents.id_ for documents in documents_ll])

    return ids, documents


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
