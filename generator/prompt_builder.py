class PromptBuilder:

    def build_prompt(self, query_code, retrieved_snippets):
        instruction = (
            "You are a Python coding assistant.\n"
            "Use the retrieved repository snippets when useful.\n"
            "Complete the following Python code.\n"
            "Only output the completed code.\n"
        )

        prompt_parts = [instruction, "\n# Retrieved repository snippets\n"]

        for snippet in retrieved_snippets:
            prompt_parts.append(f"\n# File: {snippet['file_path']}\n")
            prompt_parts.append(snippet["content"].rstrip())
            prompt_parts.append("\n")

        prompt_parts.append("\n# Code to complete\n")
        prompt_parts.append(query_code.strip())
        prompt_parts.append("\n")

        return "".join(prompt_parts)