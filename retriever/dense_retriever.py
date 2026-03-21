import math
import re
from collections import Counter

from retriever.base_retriever import BaseRetriever


class DenseRetriever(BaseRetriever):
	"""
	Lightweight dense-like retriever based on normalized term-frequency vectors.
	Keeps the project dependency-light while offering cosine-style ranking.
	"""

	def __init__(self, snippets):
		super().__init__(snippets)

	def tokenize(self, text):
		return [token.lower() for token in re.findall(r"[A-Za-z_]+", text)]

	def vectorize(self, text):
		tokens = self.tokenize(text)
		counts = Counter(tokens)

		norm = math.sqrt(sum(value * value for value in counts.values()))
		if norm == 0:
			return {}

		return {key: value / norm for key, value in counts.items()}

	def cosine_similarity(self, query_vec, doc_vec):
		if not query_vec or not doc_vec:
			return 0.0

		if len(query_vec) > len(doc_vec):
			query_vec, doc_vec = doc_vec, query_vec

		return sum(weight * doc_vec.get(token, 0.0) for token, weight in query_vec.items())

	def retrieve(self, query, top_k=5):
		query_vec = self.vectorize(query)
		scored = []

		for snippet in self.snippets:
			doc_vec = self.vectorize(snippet.get("content", ""))
			score = self.cosine_similarity(query_vec, doc_vec)
			scored.append((score, snippet))

		scored.sort(key=lambda x: x[0], reverse=True)
		return [snippet for _, snippet in scored[:top_k]]
