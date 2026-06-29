from dotenv import load_dotenv
load_dotenv(override=True)
from app.services.document_storage_service import DocumentStorageService
from app.services.embeddings_services import EmbeddingsService
from app.services.retriever_services import RetrieverService
from app.services.llm.huggingface_provider import HuggingFaceProvider
from app.services.llm.llm_service import LLMService
from prompt.rag_prompt import RAGPrompt
import traceback

try:
    doc_id = "ab1d09b8-dd95-4cc2-a0b6-e42e705e3a33"
    query = "What is this book about?"
    
    print("Loading document...")
    storage = DocumentStorageService()
    document = storage.load_document(doc_id)
    
    print("Generating query embedding...")
    emb_service = EmbeddingsService()
    query_embedding = emb_service.generate(query)
    
    print("Retrieving chunks...")
    retriever = RetrieverService()
    retrieved_chunks = retriever.retrieve(query_embedding, document["embeddings_chunks"], 3)
    
    print("Building prompt...")
    rag_context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
    prompt = RAGPrompt.build(query, rag_context)
    
    print("Generating LLM response...")
    provider = HuggingFaceProvider()
    llm = LLMService(provider)
    response = llm.generate(prompt)
    
    print("Success:", response)
except Exception as e:
    print("FAILED!")
    traceback.print_exc()
