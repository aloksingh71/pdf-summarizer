from django.apps import AppConfig
from transformers import pipeline

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    _qa_pipeline = None

    def ready(self):
        if not UsersConfig._qa_pipeline:
            print("Loading Hugging Face Model...")
            UsersConfig._qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
            print("Model Loaded Successfully!")

    @classmethod
    def get_qa_pipeline(cls):
        return cls._qa_pipeline