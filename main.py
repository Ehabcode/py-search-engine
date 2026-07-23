from pathlib import Path
import string
import math
import argparse

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


def compute_tf(token, tokens):
    return tokens.count(token) / len(tokens)


def compute_idf(token, documents):
    num_docs_with_token = 0
    for text in documents.values():
        if token in tokenize(text):
            num_docs_with_token += 1
    if num_docs_with_token == 0:
        return 0
    return math.log(len(documents) / num_docs_with_token)


def rank_results(results, query, documents):
    query_tokens = tokenize(query)
    scores = {}

    for filename in results:
        doc_tokens = tokenize(documents[filename])
        total_score = 0
        for token in query_tokens:
            tf = compute_tf(token, doc_tokens)
            idf = compute_idf(token, documents)
            total_score += tf * idf
        scores[filename] = total_score

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return ranked


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple local search engine")
    parser.add_argument("query" , nargs="+" , help="Words to search for")
    args = parser.parse_args()

    query = " ".join(args.query)
    docs = load_documents(DATA_DIR)
    index = build_index(docs)
    results = search(index, query)
    ranked = rank_results(results, query, docs)

    if not ranked:
        print("No results found.")
    else:
        for filename, score in ranked:
            print(f"{filename} (score: {score:.4f})")