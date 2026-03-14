class PromptBuilder:

    def build_prompt(self, query_code, retrieved_snippets):

        prompt = "# Retrieved repository snippets\n\n"

        for snippet in retrieved_snippets:

            prompt += f"# File: {snippet['file_path']}\n"
            prompt += snippet["content"]
            prompt += "\n\n"
            
            prompt = """
                    You are a Python coding assistant.

                    Use the retrieved repository code if helpful.

                    Complete the following Python code.

                    Only output the completed code.

                    """

            prompt += query_code

                    
            return prompt