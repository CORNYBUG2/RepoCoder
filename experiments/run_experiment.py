from evaluation.evaluator import Evaluator
from repository.file_scanner import FileScanner
from repository.loader import RepositoryLoader
from repository.sliding_window import SlidingWindowChunker
from retriever.sparse_retriever import SparseRetriever


def run_retrieval_experiment(repo_path):
	loader = RepositoryLoader(repo_path)
	files = loader.load_files()

	scanner = FileScanner()
	scanned = scanner.scan_files(files)

	chunker = SlidingWindowChunker(window_size=20, step_size=10)
	snippets = chunker.chunk_repository(scanned)

	retriever = SparseRetriever(snippets)

	test_queries = [
		{
			"query": "def train_step(x, y):\n    output = model(x)\n    loss =",
			"reference": "loss = criterion(output, y)",
		},
		{
			"query": "class RepositoryLoader:\n    def load_files(self):\n",
			"reference": "for root, dirs, files in os.walk(self.repo_path):",
		},
	]

	predictions = []
	references = []

	for item in test_queries:
		retrieved = retriever.retrieve(item["query"], top_k=1)
		predicted = retrieved[0]["content"] if retrieved else ""
		predictions.append(predicted)
		references.append(item["reference"])

	evaluator = Evaluator()
	report = evaluator.evaluate_many(predictions, references)
	return report


if __name__ == "__main__":
	import argparse
	from pathlib import Path

	parser = argparse.ArgumentParser(description="Run RepoCoder retrieval experiment")
	parser.add_argument(
		"--repo-path",
		default=str(Path(__file__).resolve().parents[1]),
		help="Path to repository to evaluate",
	)
	args = parser.parse_args()

	results = run_retrieval_experiment(args.repo_path)
	print("Experiment results:")
	print(results)
