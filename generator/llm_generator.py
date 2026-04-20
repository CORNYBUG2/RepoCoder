from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LLMGenerator:

    def __init__(self, model_name="deepseek-ai/deepseek-coder-1.3b-base"):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print("Using device:", self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        model_kwargs = {}
        if self.device == "cuda":
            model_kwargs["torch_dtype"] = torch.float16
            model_kwargs["device_map"] = "auto"

        self.model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)

        if self.device == "cpu":
            self.model.to("cpu")

    def generate(self, prompt, max_tokens=120, temperature=0.0):

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        ).to(self.model.device)

        do_sample = temperature > 0

        generate_kwargs = {
            "max_new_tokens": max_tokens,
            "do_sample": do_sample,
            "eos_token_id": self.tokenizer.eos_token_id,
        }

        if do_sample:
            generate_kwargs["temperature"] = temperature

        with torch.no_grad():
            outputs = self.model.generate(**inputs, **generate_kwargs)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        input_ids = inputs["input_ids"]
        generated_ids = outputs[0][input_ids.shape[-1]:]

        generated = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        generated = generated.strip().split("\n")[0]

        return generated.strip()