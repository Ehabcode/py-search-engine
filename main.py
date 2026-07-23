from pathlib import Path
import string

DATA_DIR = Path("data")


def load_documents(data_dir):
    documents = {}
    for file_path in data_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            documents[file_path.name] = content
    return documents


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


def search(index, query):
    query_tokens = tokenize(query)
    if not query_tokens:
        return set()

    result = index.get(query_tokens[0], set())
    for token in query_tokens[1:]:
        result = result & index.get(token, set())
    return result


if __name__ == "__main__":
    docs = load_documents(DATA_DIR)
    index = build_index(docs)

    results = search(index, "python language")
    print(results)