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
        text = text.replace(punctuation_mark, "")
    tokens = text.split()
    return tokens


if __name__ == "__main__":
    docs = load_documents(DATA_DIR)
    for filename, text in docs.items():
        print(f"--- {filename} ---")
        tokens = tokenize(text)
        print(tokens)
        print()

