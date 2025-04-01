# backend/app/processors/code_processor.py
from transformers import pipeline

class CodeProcessor:
    def __init__(self):
        self.generator = pipeline("text-generation", model="Salesforce/codegen-16B-mono")

    async def process(self, prompt: str):
        result = self.generator(
            f"# {prompt}\n",
            max_length=200,
            temperature=0.7,
            do_sample=True
        )
        
        return {
            "type": "code",
            "language": "python",
            "data": result[0]['generated_text']
        }