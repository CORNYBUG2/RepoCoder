class PromptBuilder:

    def build_prompt(self, query_code, retrieved_snippets):
        instruction = (
            "You are a Python code completion engine.\n"
            "Complete ONLY the missing part of the given code.\n"
            "Do NOT add new functions, imports, or explanations.\n"
            "Do NOT rewrite existing code.\n"
            "Only fill the missing expression after 'loss ='.\n"
            "Return the full function with the completion inserted.\n"
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
    
    def build_completion_prompt(self, query_code):
        return (
            "Complete only the missing part of the code.\n"
            "Do not add anything else.\n\n"
            + query_code.strip()
        )