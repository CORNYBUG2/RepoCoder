from evaluation.metrics import exact_match_score, similarity_ratio, line_overlap_f1


class Evaluator:
	def evaluate_one(self, prediction, reference):
		return {
			"exact_match": exact_match_score(prediction, reference),
			"similarity": similarity_ratio(prediction, reference),
			"line_f1": line_overlap_f1(prediction, reference),
		}

	def evaluate_many(self, predictions, references):
		if len(predictions) != len(references):
			raise ValueError("Predictions and references must have equal length")

		rows = [self.evaluate_one(pred, ref) for pred, ref in zip(predictions, references)]

		if not rows:
			return {
				"count": 0,
				"avg_exact_match": 0.0,
				"avg_similarity": 0.0,
				"avg_line_f1": 0.0,
				"details": [],
			}

		count = len(rows)
		return {
			"count": count,
			"avg_exact_match": sum(row["exact_match"] for row in rows) / count,
			"avg_similarity": sum(row["similarity"] for row in rows) / count,
			"avg_line_f1": sum(row["line_f1"] for row in rows) / count,
			"details": rows,
		}
