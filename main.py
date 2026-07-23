from pathlib import Path


DATA_DIR = Path("data")


def load_documents(data_dir):
    documents = {}
    for file_path in data_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            documents[file_path.name] = content
    return documents


import string

def tokenize(text):
    text = text.lower()
    for punctuation_mark in string.punctuation:
        text = text.replace(punctuation_mark, " ")
    tokens = text.split()
    return tokens


def build_index(documents):
    index = {}
    for filename, text in documents.items():
        tokens = tokenize(text)
        for token in tokens:
            if token not in index:
                index[token] = set()
            index[token].add(filename)
    return index


if __name__ == "__main__":
    docs = load_documents(DATA_DIR)
    index = build_index(docs)
    for word, files in index.items():
        print(f"{word}: {files}")





 
