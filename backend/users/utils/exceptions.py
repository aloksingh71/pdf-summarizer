class SummarizationError(Exception):
    """Base exception for summarization-related errors."""
    def __init__(self, message="An error occurred during summarization"):
        self.message = message
        super().__init__(self.message)

class FileProcessingError(SummarizationError):
    """Raised when file processing (e.g., PDF extraction) fails."""
    def __init__(self, message="Failed to process the uploaded file"):
        super().__init__(message)

class TextExtractionError(SummarizationError):
    """Raised when no text can be extracted from the file."""
    def __init__(self, message="No text could be extracted from the file"):
        super().__init__(message)

class APIRequestError(SummarizationError):
    """Raised when the Mistral API request fails."""
    def __init__(self, message="Failed to communicate with the summarization API"):
        super().__init__(message)