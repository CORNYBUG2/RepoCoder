import os
import math
from collections import Counter, defaultdict


class SparseRetriever:

    def __init__(self, base_path):
        self.base_path = base_path

        self.documents = []
        self.doc_freq = defaultdict(int)
        self.doc_term_counts = []
        self.N = 0

        self.EXCLUDE_DIRS = {"repoenv", "venv", ".git", "__pycache__", "site-packages"}

        self.STOPWORDS = {
            "def", "return", "import", "from", "class", "self",
            "for", "while", "if", "else", "try", "except"
        }

        self._index_repository()

    def _tokenize(self, text):
        return [
            t for t in text.lower().split()
            if t not in self.STOPWORDS and len(t) > 2
        ]

    def _chunk_text(self, text, size=300, overlap=50):
        lines = text.split("\n")
        chunks = []
        for i in range(0, len(lines), size - overlap):
            chunk = "\n".join(lines[i:i + size])
            chunks.append(chunk)
        return chunks

    def _index_repository(self):

        for root, dirs, files in os.walk(self.base_path):

            dirs[:] = [d for d in dirs if d not in self.EXCLUDE_DIRS]

            for file in files:
                if not file.endswith(".py"):
                    continue

                file_path = os.path.join(root, file)

                if any(excluded in file_path for excluded in self.EXCLUDE_DIRS):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                except:
                    continue

                chunks = self._chunk_text(text)

                for chunk in chunks:
                    tokens = self._tokenize(chunk)
                    term_counts = Counter(tokens)

                    self.documents.append({
                        "path": file_path,
                        "content": chunk,
                        "tokens": tokens
                    })

                    self.doc_term_counts.append(term_counts)

                    for term in term_counts.keys():
                        self.doc_freq[term] += 1

        self.N = len(self.documents)

    def _tf_idf(self, term, term_counts):
        tf = term_counts[term]
        df = self.doc_freq.get(term, 1)
        idf = math.log((self.N + 1) / (df + 1)) + 1
        return tf * idf

    def retrieve(self, query, top_k=3):

        query_tokens = self._tokenize(query)
        query_counts = Counter(query_tokens)

        scores = []

        for idx, doc in enumerate(self.documents):
            score = 0
            term_counts = self.doc_term_counts[idx]

            for term in query_counts:
                if term in term_counts:
                    score += self._tf_idf(term, term_counts) * query_counts[term]

            if score > 0:
                scores.append({
                    "file_path": doc["path"],
                    "content": doc["content"],
                    "score": score
                })

        scores.sort(key=lambda x: x["score"], reverse=True)

        return scores[:top_k]