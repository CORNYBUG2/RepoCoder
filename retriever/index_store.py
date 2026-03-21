import json


class IndexStore:
	"""Simple snippet index persistence layer."""

	def __init__(self):
		self._snippets = []

	def build(self, snippets):
		self._snippets = list(snippets)

	def get_snippets(self):
		return self._snippets

	def save(self, path):
		with open(path, "w", encoding="utf-8") as file:
			json.dump(self._snippets, file, ensure_ascii=False)

	def load(self, path):
		with open(path, "r", encoding="utf-8") as file:
			self._snippets = json.load(file)

		return self._snippets
