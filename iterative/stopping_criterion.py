class StoppingCriterion:
	def __init__(self, max_iterations=2, min_delta_chars=5):
		self.max_iterations = max_iterations
		self.min_delta_chars = min_delta_chars

	def should_stop(self, iteration, previous_output, current_output):
		if iteration >= self.max_iterations:
			return True

		if current_output is None:
			return True

		if previous_output is None:
			return False

		if previous_output.strip() == current_output.strip():
			return True

		delta = abs(len(current_output) - len(previous_output))
		return delta < self.min_delta_chars
