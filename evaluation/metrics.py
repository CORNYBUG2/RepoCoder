from difflib import SequenceMatcher


def normalize(text):
	return "\n".join(line.rstrip() for line in text.strip().splitlines())


def exact_match_score(prediction, reference):
	return float(normalize(prediction) == normalize(reference))


def similarity_ratio(prediction, reference):
	pred = normalize(prediction)
	ref = normalize(reference)
	return SequenceMatcher(a=pred, b=ref).ratio()


def line_overlap_f1(prediction, reference):
	pred_lines = [line.strip() for line in normalize(prediction).splitlines() if line.strip()]
	ref_lines = [line.strip() for line in normalize(reference).splitlines() if line.strip()]

	if not pred_lines and not ref_lines:
		return 1.0
	if not pred_lines or not ref_lines:
		return 0.0

	pred_set = set(pred_lines)
	ref_set = set(ref_lines)

	overlap = len(pred_set.intersection(ref_set))
	precision = overlap / len(pred_set) if pred_set else 0.0
	recall = overlap / len(ref_set) if ref_set else 0.0

	if precision + recall == 0:
		return 0.0

	return 2 * precision * recall / (precision + recall)
