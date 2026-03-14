class SlidingWindowChunker:
    def __init__(self, window_size=20, step_size=10):
        self.window_size = window_size
        self.step_size = step_size

    def chunk_file(self, scanned_file):
        """
        Convert one scanned file into snippets
        """

        lines = scanned_file["lines"]
        file_path = scanned_file["file_path"]

        snippets = []

        total_lines = len(lines)

        for start in range(0, total_lines, self.step_size):

            end = min(start + self.window_size, total_lines)

            snippet_lines = lines[start:end]

            if not snippet_lines:
                continue

            content = "".join(snippet_lines)

            snippet = {
                "file_path": file_path,
                "start_line": start + 1,
                "end_line": end,
                "content": content,
                "tokens": set(content.split())
            }

            snippets.append(snippet)

            if end == total_lines:
                break

        return snippets

    def chunk_repository(self, scanned_files):
        """
        Convert entire repo into snippets
        """

        all_snippets = []

        for file in scanned_files:
            file_snippets = self.chunk_file(file)
            all_snippets.extend(file_snippets)

        return all_snippets