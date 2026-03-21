from iterative.query_constructor import QueryConstructor
from iterative.stopping_criterion import StoppingCriterion


class IterationController:

    def __init__(
        self,
        retriever,
        prompt_builder,
        generator,
        max_iterations=2,
        top_k=3,
        max_tokens=120,
        temperature=0.0,
    ):

        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.generator = generator
        self.query_constructor = QueryConstructor()
        self.stopping_criterion = StoppingCriterion(max_iterations=max_iterations)
        self.top_k = top_k
        self.max_tokens = max_tokens
        self.temperature = temperature

    def run(self, query_code):
        previous_output = None
        current_query = query_code
        current_output = ""

        for iteration in range(1, self.stopping_criterion.max_iterations + 1):

            # FIX: stronger retrieval query
            search_query = current_query + " python function implementation logic return"

            results = self.retriever.retrieve(search_query, top_k=self.top_k)

            prompt = self.prompt_builder.build_prompt(current_query, results)
    
            current_output = self.generator.generate(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            if self.stopping_criterion.should_stop(iteration, previous_output, current_output):
                break

            previous_output = current_output
            current_query = self.query_constructor.construct_query(query_code, current_output)

        return current_output