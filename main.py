import argparse
from pathlib import Path

from repository.loader import RepositoryLoader
from repository.file_scanner import FileScanner
from repository.sliding_window import SlidingWindowChunker
from retriever.sparse_retriever import SparseRetriever
from generator.prompt_builder import PromptBuilder
from generator.llm_generator import LLMGenerator
from iterative.iteration_controller import IterationController


def main():
    parser = argparse.ArgumentParser(description="Run RepoCoder prototype pipeline")
    parser.add_argument(
        "--repo-path",
        default=str(Path(__file__).resolve().parent),
        help="Path to repository that should be indexed",
    )
    args = parser.parse_args()

    repo_path = args.repo_path

    # --- index repository ---
    loader = RepositoryLoader(repo_path)
    files = loader.load_files()

    scanner = FileScanner()
    scanned_files = scanner.scan_files(files)

    chunker = SlidingWindowChunker(window_size=20, step_size=10)
    snippets = chunker.chunk_repository(scanned_files)

    retriever = SparseRetriever(snippets)

    # code we want to complete
    query_code = """
def train_step(x, y):
    output = model(x)
    loss =
"""

    # components
    builder = PromptBuilder()
    generator = LLMGenerator()

    controller = IterationController(retriever, builder, generator)

    # run RepoCoder pipeline
    final_output = controller.run(query_code)

    print("\nFinal generated code:\n")
    print(final_output[-400:])

# main function

if __name__ == "__main__":
    main()