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

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        do_sample = temperature > 0
        generate_kwargs = {
            "max_new_tokens": max_tokens,
            "do_sample": do_sample,
        }
        if do_sample:
            generate_kwargs["temperature"] = temperature

        outputs = self.model.generate(**inputs, **generate_kwargs)

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)