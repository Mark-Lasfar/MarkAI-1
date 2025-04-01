# backend/ai/document_processor.py
from transformers import pipeline
from PyPDF2 import PdfReader

class DocumentAI:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.qa_pipeline = pipeline("question-answering", model="bert-large-uncased")

    def process_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        
        summary = self.summarizer(text, max_length=150, min_length=30, do_sample=False)
        return {
            'full_text': text,
            'summary': summary[0]['summary_text']
        }