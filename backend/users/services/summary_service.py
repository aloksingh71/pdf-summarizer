import logging
from django.core.cache import cache
from ..utils.mistral_client import MistralClient
from ..utils.pdf_utils import extract_text_from_pdf
from ..utils.summarizer_factory import SummarizerFactory
from ..repositories.summary_repository import SummaryRepository
from ..repositories.file_repository import FileRepository
from ..utils.exceptions import SummarizationError, FileProcessingError, TextExtractionError, APIRequestError

logger = logging.getLogger(__name__)

class SummaryService:
    def __init__(self):
        self.mistral_client = MistralClient.get_instance()  
        self.factory = SummarizerFactory()
        self.repo = SummaryRepository()

    def generate_summary(self, uploaded_file_id, user, summary_type, num_points, paragraph_length):
        """
          Generate a summary for the uploaded file using cache if available.
         Raises specific exceptions for different failure scenarios.
        """
        cache_key = f"summary_{uploaded_file_id}_{summary_type}_{num_points}_{paragraph_length}"
        

        cached_summary_text = cache.get(cache_key)
        file_repo = FileRepository()

        try:
            # Step 1: Retrieve the file (needed whether cached or not)
            uploaded_file = file_repo.get_file(uploaded_file_id, user)
        except Exception as e:
            logger.error(f"File retrieval failed for ID {uploaded_file_id}, user {user.id}: {str(e)}")
            raise FileProcessingError(f"File with ID {uploaded_file_id} not found or inaccessible")

        if cached_summary_text:
            # Cached summary found: Save it to history
            logger.info(f"Retrieved cached summary for key: {cache_key}")
            summary_data = {
                'uploaded_file': uploaded_file,
                'summary_type': summary_type,
                'num_points': num_points if summary_type == "bullet" else None,
                'paragraph_length': paragraph_length if summary_type == "paragraph" else None,
                'summary_text': cached_summary_text 
            }
            try:
                summary = self.repo.save_summary(summary_data)
                logger.info(f"Cached summary saved to history for file ID {uploaded_file_id}")
                return summary
            except Exception as e:
                logger.error(f"Failed to save cached summary: {str(e)}", exc_info=True)
                raise SummarizationError("Failed to save the cached summary")

        try:
            # Step 2: Extract text from PDF
            try:
                text = extract_text_from_pdf(uploaded_file.file.path)
                if not text:
                    logger.warning(f"No text extracted from file {uploaded_file.file.path}")
                    raise TextExtractionError()
            except Exception as e:
                logger.error(f"PDF extraction failed for {uploaded_file.file.path}: {str(e)}", exc_info=True)
                raise FileProcessingError(f"Failed to process PDF: {str(e)}")

            # Step 3: Generate summary using Factory + Strategy
            try:
                summarizer = self.factory.get_summarizer(summary_type)
                summary_text = summarizer.summarize(self.mistral_client, text, num_points, paragraph_length)
            except ValueError as e:
                logger.error(f"Invalid summary type {summary_type}: {str(e)}")
                raise SummarizationError(f"Invalid summary type: {summary_type}")
            except Exception as e:
                logger.error(f"API summarization failed: {str(e)}", exc_info=True)
                raise APIRequestError()

            # Step 4: Save summary and cache it
            summary_data = {
                'uploaded_file': uploaded_file,
                'summary_type': summary_type,
                'num_points': num_points if summary_type == "bullet" else None,
                'paragraph_length': paragraph_length if summary_type == "paragraph" else None,
                'summary_text': summary_text
            }
            try:
                summary = self.repo.save_summary(summary_data)
                logger.info(f"Summary generated and saved for file ID {uploaded_file_id}")
                cache.set(cache_key, summary_text, timeout=3600)  # Cache only the text
                logger.info(f"Cached summary with key: {cache_key}")
                return summary
            except Exception as e:
                logger.error(f"Failed to save summary: {str(e)}", exc_info=True)
                raise SummarizationError("Failed to save the generated summary")

        except SummarizationError as e:
            raise e
        except Exception as e:
            logger.critical(f"Unexpected error in summary generation: {str(e)}", exc_info=True)
            raise SummarizationError("An unexpected error occurred during summarization")

    def answer_question(self, summary_id, user, question):
        """
        Answer a question based on a summary.
        """
        try:
            summary = self.repo.get_summary(summary_id, user)
            answer = self.mistral_client.answer_question(summary.summary_text, question)
            logger.info(f"Question answered for summary ID {summary_id}")
            return {"summary_id": summary_id, "question": question, "answer": answer}
        except Exception as e:
            logger.error(f"Failed to answer question for summary ID {summary_id}: {str(e)}", exc_info=True)
            raise SummarizationError("Failed to process your question")