class QueryConstructor:

    def __init__(self, window_size=20):
        self.window_size = window_size

    def construct_query(self, original_code, generated_code):

        original_lines = original_code.strip().split("\n")
        generated_lines = generated_code.strip().split("\n")

        original_tail = original_lines[-self.window_size:]
        generated_head = generated_lines[:self.window_size]

        query_lines = original_tail + generated_head

        return "\n".join(query_lines)