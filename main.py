import argparse
from pathlib import Path

import yaml

from repository.loader import RepositoryLoader
from repository.file_scanner import FileScanner
from repository.sliding_window import SlidingWindowChunker
from retriever.dense_retriever import DenseRetriever
from retriever.sparse_retriever import SparseRetriever
from generator.prompt_builder import PromptBuilder
from generator.llm_generator import LLMGenerator
from iterative.iteration_controller import IterationController


def _merge_dict(base, override):
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_path):
    defaults = {
        "repo": {"path": "."},
        "chunking": {"window_size": 20, "step_size": 10},
        "retrieval": {"type": "sparse", "top_k": 3},
        "generation": {
            "model_name": "deepseek-ai/deepseek-coder-1.3b-base",
            "max_tokens": 120,
            "temperature": 0.0,
        },
        "iteration": {"max_iterations": 2},
    }

    path = Path(config_path)
    if not path.exists():
        return defaults

    with open(path, "r", encoding="utf-8") as file:
        loaded = yaml.safe_load(file) or {}

    return _merge_dict(defaults, loaded)

def build_retriever(retrieval_type, snippets):
    retrieval_type = (retrieval_type or "sparse").lower()

    if retrieval_type == "dense":
        return DenseRetriever(snippets)

    return SparseRetriever("D:\\Repocoder\\repocoder")


def main():
    parser = argparse.ArgumentParser(description="Run RepoCoder prototype pipeline")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parent / "config" / "config.yaml"),
        help="Path to YAML config file",
    )
    parser.add_argument(
        "--repo-path",
        default=None,
        help="Path to repository that should be indexed",
    )
    args = parser.parse_args()

    config = load_config(args.config)

    repo_path = args.repo_path or config["repo"]["path"]

    if repo_path == ".":
        repo_path = str(Path(__file__).resolve().parent)

    chunk_cfg = config["chunking"]
    retrieval_cfg = config["retrieval"]
    generation_cfg = config["generation"]
    iteration_cfg = config["iteration"]

    # --- index repository ---
    loader = RepositoryLoader(repo_path)
    files = loader.load_files()

    scanner = FileScanner()
    scanned_files = scanner.scan_files(files)

    chunker = SlidingWindowChunker(
        window_size=chunk_cfg["window_size"],
        step_size=chunk_cfg["step_size"],
    )
    snippets = chunker.chunk_repository(scanned_files)

    retriever = build_retriever(retrieval_cfg.get("type"), snippets)

    # code we want to complete
    query_code = """
def train_step(x, y):
    output = model(x)
    loss =
"""

    # components
    builder = PromptBuilder()
    generator = LLMGenerator(model_name=generation_cfg["model_name"])

    controller = IterationController(
        retriever,
        builder,
        generator,
        max_iterations=iteration_cfg["max_iterations"],
        top_k=retrieval_cfg["top_k"],
        max_tokens=generation_cfg["max_tokens"],
        temperature=generation_cfg["temperature"],
    )

    # run RepoCoder pipeline
    final_output = controller.run(query_code)

    print("\nFinal generated code:\n")
    print(final_output[-400:])

# main function

if __name__ == "__main__":
    main()