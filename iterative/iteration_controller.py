class IterationController:

    def __init__(self, retriever, prompt_builder, generator):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.generator = generator

    def run(self, query_code):

        # First retrieval
        results = self.retriever.retrieve(query_code, top_k=3)

        prompt = self.prompt_builder.build_prompt(query_code, results)

        first_generation = self.generator.generate(prompt)

        # Second retrieval using generated output
        results2 = self.retriever.retrieve(first_generation, top_k=3)

        prompt2 = self.prompt_builder.build_prompt(query_code, results2)

        final_generation = self.generator.generate(prompt2)

        return final_generation