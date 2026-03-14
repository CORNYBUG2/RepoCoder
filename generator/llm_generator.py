from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LLMGenerator:

    def __init__(self, model_name="Salesforce/codegen-350M-mono"):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print("Using device:", self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )

        self.model.to(self.device)

    def generate(self, prompt, max_tokens=120):

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
            do_sample=True
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)