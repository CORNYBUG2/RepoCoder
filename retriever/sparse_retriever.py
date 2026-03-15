import re


class SparseRetriever:

    def __init__(self, snippets):
        self.snippets = snippets

    # Better tokenizer
    def tokenize(self, text):

        words = re.findall(r"[A-Za-z_]+", text)

        tokens = set()

        for w in words:
            w = w.lower()
            tokens.add(w)
            tokens.update(w.split("_"))

        return tokens

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

            # re-tokenize snippet content using improved tokenizer
            snippet_tokens = self.tokenize(snippet["content"])

            score = self.jaccard_similarity(query_tokens, snippet_tokens)

            # boost score if important keywords appear
            if "loss" in snippet_tokens:
                score += 0.3

            scored_snippets.append((score, snippet))

        scored_snippets.sort(key=lambda x: x[0], reverse=True)

        # Debug output
        print("\nTop retrieved snippets:")
        for score, snippet in scored_snippets[:top_k]:
            print(score, snippet["file_path"])

        return [s[1] for s in scored_snippets[:top_k]]