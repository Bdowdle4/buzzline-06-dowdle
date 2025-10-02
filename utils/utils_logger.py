# Reusable logger setup for EDM Buzzline project.
# Provides a standardized logger format for both producer and consumer.
import logging
import sys

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create and return a logger with a standard format.
    
    Args:
        name (str): The name of the logger (usually __name__ of the calling module).
        level (int): Logging level (default: logging.INFO).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger is called multiple times
    if not logger.handlers:
        # StreamHandler for console output
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Formatter with timestamp, module, level, and message
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

    return logger


# Example usage for testing
if __name__ == "__main__":
    log = get_logger("test_logger", logging.DEBUG)
    log.debug("This is a DEBUG message for testing.")
    log.info("This is an INFO message for testing.")
    log.warning("This is a WARNING message for testing.")
    log.error("This is an ERROR message for testing.")