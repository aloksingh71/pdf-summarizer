import functools
import logging

logger = logging.getLogger(__name__)

def log_api_call(max_length=100):
    """
    Decorator to log function calls with truncated arguments for readability.
    
    Args:
        max_length (int): Maximum length of string arguments before truncation (default: 100).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            concise_args = []
            for arg in args[1:]: 
                if isinstance(arg, str) and len(arg) > max_length:
                    concise_args.append(f"{arg[:max_length]}... (truncated, {len(arg)} chars)")
                else:
                    concise_args.append(str(arg))

            logger.info(f"Calling {func.__name__} with args: {concise_args}, kwargs: {kwargs}")
            
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator