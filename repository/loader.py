import os


class RepositoryLoader:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.ignore_dirs = {".git", "__pycache__", ".venv", "venv", "node_modules"}

    def load_files(self):
        python_files = []

        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    python_files.append(full_path)

        return python_files


if __name__ == "__main__":

    repo_path = r"D:\Repocoder\repocoder"

    print("Checking path:", repo_path)
    print("Exists:", os.path.exists(repo_path))

    loader = RepositoryLoader(repo_path)

    files = loader.load_files()

    print(f"\nFound {len(files)} Python files:\n")
    for f in files:
        print(f)