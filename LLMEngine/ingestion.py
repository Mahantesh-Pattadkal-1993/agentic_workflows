from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import os
from pdf_reader import PDFReader  # Import our PDFReader class
from dotenv import load_dotenv
from qdrant import QdrantDB

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# 1. Function to read the document


class IngestDocument:
    _instance = None

    def __new__(cls, filepath="localhost"):
        """Create a single instance of QdrantManager (singleton pattern)."""
        if cls._instance is None:

            cls._instance = super(IngestDocument, cls).__new__(cls)
            # Initialize attributes only once when the instance is first created
            cls._instance.qdrant_service = QdrantDB()


        return cls._instance


    def get_text(self):
        # return text
        pass

    def get_chunks(self):
        # return chunks listy
        pass

    def write_to_qdrant(self):
        #qdrantservice
        pass
    
    
    def ingest_document():
        pass
        
        # call get text
        # call get_chgunks
        # call write to qdrant

