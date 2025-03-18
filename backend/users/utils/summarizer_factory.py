from abc import ABC, abstractmethod

class Summarizer(ABC):
    @abstractmethod
    def summarize(self, client, text, num_points, paragraph_length):
        pass

class BulletSummarizer(Summarizer):
    def summarize(self, client, text, num_points, paragraph_length):
        return client.summarize(text, "bullet", num_points=num_points)

class ParagraphSummarizer(Summarizer):
    def summarize(self, client, text, num_points, paragraph_length):
        return client.summarize(text, "paragraph", paragraph_length=paragraph_length)

class SummarizerFactory:
    def get_summarizer(self, summary_type):
        if summary_type == "bullet":
            return BulletSummarizer()
        elif summary_type == "paragraph":
            return ParagraphSummarizer()
        raise ValueError("Invalid summary type")