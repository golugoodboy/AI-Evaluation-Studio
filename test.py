from dotenv import load_dotenv
load_dotenv(override=True)
import traceback
from app.api.rag import rag_service

try:
    print(rag_service.process_query('What is this book about?', 'ab1d09b8-dd95-4cc2-a0b6-e42e705e3a33'))
except Exception as e:
    traceback.print_exc()
