from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import os
from pdf_reader import PDFReader  # Import our PDFReader class
from dotenv import load_dotenv
from qdrant import QdrantDB
from pdf_reader import PDFReader

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# 1. Function to read the document


class IngestDocument:
    _instance = None

    def __new__(cls, filepath="path"):
        """Create a single instance of QdrantManager (singleton pattern)."""
        if cls._instance is None:

            cls._instance = super(IngestDocument, cls).__new__(cls)
            # Initialize attributes only once when the instance is first created
            cls._instance.qdrant_service = QdrantDB()
            cls._instance.pdfreader = PDFReader(filepath)
            


        return cls._instance


    def get_text(self):
        text =  self.pdfreader.get_all_text()
        return text

    def get_chunks(self, text):
        chunks = self.pdfreader.get_chunks(text)
        return chunks


    def write_to_qdrant(self,chuncklist):
        self.qdrant_service.upsert_chunks(chunkList)
                
    
    
    
    def ingest_document(self):
        self.qdrant_service.check_and_create_collection()
        text = self.get_text()
        chunkList = self.get_chunks(text)


