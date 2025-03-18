import os
import requests
from ..utils.logging_decorator import log_api_call

class MistralClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MistralClient, cls).__new__(cls)
            cls._instance.api_key = os.getenv("MISTRAL_API_KEY")
            cls._instance.api_url = "https://api.mistral.ai/v1/chat/completions"
            if not cls._instance.api_key:
                raise ValueError("Mistral AI API Key is missing.")
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls.__new__(cls)

    @log_api_call(max_length=50)
    def _call_api(self, prompt, system_message="You are a helpful AI assistant."):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "model": "mistral-medium",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def summarize(self, text, summary_type="paragraph", num_points=5, paragraph_length=100):
        if summary_type == "bullet":
            prompt = f"Summarize the following text in {num_points} bullet points:\n{text}"
        else:
            prompt = f"Summarize this text in approximately {paragraph_length} words:\n{text}"
        return self._call_api(prompt, "You are a helpful AI assistant that summarizes text.")

    def answer_question(self, summary_text, question):
        prompt = f"Based on the following summary, answer the question concisely:\n\nSummary:\n{summary_text}\n\nQuestion: {question}"
        return self._call_api(prompt, "You are an AI that answers questions based on provided summaries.")