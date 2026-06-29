class PDFProcessingError(Exception):
    """Custom exception for PDF processing errors."""
    pass


class ChunkProcessingError(Exception):
    """Custom exception for Chunk processing errors."""
    pass    


class EmbeddingProcessingError(Exception):
    """Custom exception for Embedding errors."""
    pass

class LLMProcessingError(Exception):
    """Custom exception for LLM processing errors."""
    pass

class RetrieverProcessingError(Exception):
    """Custom exception for Retriever errors."""
    pass


class RAGProcessingError(Exception):
    """Custom exception for RAG processing errors."""
    pass


class DocumentStorageError(Exception):
    """Custom exception for Document Storage errors."""
    pass