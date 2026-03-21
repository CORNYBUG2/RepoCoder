from abc import ABC, abstractmethod


class BaseRetriever(ABC):
	"""Common interface for snippet retrievers."""

	def __init__(self, snippets):
		self.snippets = snippets

	@abstractmethod
	def retrieve(self, query, top_k=5):
		raise NotImplementedError
