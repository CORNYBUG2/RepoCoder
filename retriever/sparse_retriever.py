class SparseRetriever:
    def __init__(self, snippets):
        self.snippets = snippets

    def tokenize(self, text):
        return set(text.split())

    def jaccard_similarity(self, set1, set2):

        if not set1 or not set2:
            return 0

        intersection = set1.intersection(set2)
        union = set1.union(set2)

        return len(intersection) / len(union)

    def retrieve(self, query, top_k=5):

        query_tokens = self.tokenize(query)

        scored_snippets = []

        for snippet in self.snippets:

            score = self.jaccard_similarity(query_tokens, snippet["tokens"])

            scored_snippets.append((score, snippet))

        scored_snippets.sort(key=lambda x: x[0], reverse=True)

        return [s[1] for s in scored_snippets[:top_k]]