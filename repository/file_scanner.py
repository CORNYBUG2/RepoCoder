import os


class FileScanner:
    def __init__(self):
        pass

    def scan_file(self, file_path):
        """
        Reads a file and returns its content as ordered lines
        """

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        return {
            "file_path": file_path,
            "lines": lines
        }

    def scan_files(self, file_paths):
        """
        Scan multiple files
        """

        scanned_files = []

        for path in file_paths:
            scanned_files.append(self.scan_file(path))

        return scanned_files