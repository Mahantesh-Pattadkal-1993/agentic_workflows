from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import os
import logging
from .pdf_reader import PDFReader  # Correct relative import
from dotenv import load_dotenv
from .qdrant import QdrantDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# 1. Function to read the document


class IngestDocument:
    _instance = None

    def __new__(cls, filepath="path"):
        """Create a single instance of QdrantManager (singleton pattern)."""
        if cls._instance is None:
            logger.info(f"Creating new IngestDocument instance with filepath: {filepath}")
            cls._instance = super(IngestDocument, cls).__new__(cls)
            # Initialize attributes only once when the instance is first created
            cls._instance.qdrant_service = QdrantDB()
            cls._instance.pdfreader = PDFReader(filepath)
            


        return cls._instance


    def get_text(self):
        logger.info("Extracting text from PDF document")
        text =  self.pdfreader.get_all_text()
        logger.debug(f"Extracted text length: {len(text)} characters")
        return text

    def get_chunks(self, text):
        logger.info("Splitting text into chunks")
        chunks = self.pdfreader.get_chunks(text)
        logger.info(f"Created {len(chunks)} chunks from the text")
        return chunks


    def write_to_qdrant(self,chuncklist):
        logger.info(f"Writing {len(chuncklist)} chunks to Qdrant database")
        self.qdrant_service.upsert_chunks(chuncklist)
        logger.info("Successfully wrote chunks to database")
                
    
    
    
    def ingest_document(self):
        logger.info("Starting document ingestion process")
        try:
            self.qdrant_service.check_and_create_collection()
            text = self.get_text()
            chunkList = self.get_chunks(text)
            self.write_to_qdrant(chunkList)
            logger.info("Document ingestion completed successfully")
        except Exception as e:
            logger.error(f"Error during document ingestion: {str(e)}", exc_info=True)
            raise


