from iterative.query_constructor import QueryConstructor


class IterationController:

    def __init__(self, retriever, prompt_builder, generator):

        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.generator = generator
        self.query_constructor = QueryConstructor()

    def run(self, query_code):

        # First pass
        results = self.retriever.retrieve(query_code, top_k=3)
        prompt = self.prompt_builder.build_prompt(query_code, results)

        first_generation = self.generator.generate(prompt)

        # Construct second query
        new_query = self.query_constructor.construct_query(
            query_code,
            first_generation
        )

        # Second retrieval
        results2 = self.retriever.retrieve(new_query, top_k=3)
        prompt2 = self.prompt_builder.build_prompt(query_code, results2)

        final_generation = self.generator.generate(prompt2)

        return final_generation