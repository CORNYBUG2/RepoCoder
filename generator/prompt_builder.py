class PromptBuilder:

    def build_prompt(self, query_code, retrieved_snippets):
        instruction = (
            "You are a Python coding assistant.\n"
            "Use snippets only for understanding.\n"
            "Do NOT copy or repeat any snippet.\n"
            "Write fresh code to complete the task.\n"
            "Output ONLY the final completed code.\n"
        )

        prompt_parts = [instruction, "\n### RETRIEVED SNIPPETS\n"]

        for snippet in retrieved_snippets:
            prompt_parts.append(f"\n### FILE: {snippet['file_path']}\n")
            prompt_parts.append(snippet["content"][:1200].rstrip())
            prompt_parts.append("\n### END FILE\n")

        prompt_parts.append("\n### TASK\n")
        prompt_parts.append(query_code.strip())
        prompt_parts.append("\n")

        return "".join(prompt_parts)