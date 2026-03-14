from repository.loader import RepositoryLoader
from repository.file_scanner import FileScanner
from repository.sliding_window import SlidingWindowChunker
from retriever.sparse_retriever import SparseRetriever
from generator.prompt_builder import PromptBuilder
from generator.llm_generator import LLMGenerator


def main():

    repo_path = r"D:\Repocoder\repocoder"

    loader = RepositoryLoader(repo_path)
    files = loader.load_files()

    scanner = FileScanner()
    scanned_files = scanner.scan_files(files)

    chunker = SlidingWindowChunker(window_size=20, step_size=10)
    snippets = chunker.chunk_repository(scanned_files)

    retriever = SparseRetriever(snippets)

    query = "loss ="
    results = retriever.retrieve(query, top_k=3)

    # user code we want to complete
    query_code = """
def train_step(x, y):
    output = model(x)
    loss =
"""

    # ---- build prompt ----
    builder = PromptBuilder()
    prompt = builder.build_prompt(query_code, results)

    print("\nPrompt sent to model:\n")
    print(prompt[:400])

    # ---- generate completion ----
    generator = LLMGenerator()
    generated_output = generator.generate(prompt)

    print("\nGenerated completion:\n")
    print(generated_output[-400:])


if __name__ == "__main__":
    main()