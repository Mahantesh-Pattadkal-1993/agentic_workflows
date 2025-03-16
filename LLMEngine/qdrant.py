from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import os
from pdf_reader import PDFReader  # Import our PDFReader class
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# 1. Function to read the document
def read_document(file_path):
    pdf_reader = PDFReader(file_path)
    if pdf_reader.open_pdf():
        try:
            text = pdf_reader.get_all_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
        finally:
            pdf_reader.close()
    return None

# 2. Main function to process and store vectors
def process_document_to_qdrant(file_path, collection_name="document_vectors"):
    # Initialize components
    # Note: You'll need an OpenAI API key for embeddings
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Adjust based on your needs
        chunk_overlap=200,  # Adjust overlap as needed
        length_function=len,
    )
    
    # Initialize Qdrant client (assuming it's running locally)
    qdrant_client = QdrantClient("localhost", port=6333)

    # Read document
    document_text = read_document(file_path)
    
    # Split document into chunks
    chunks = text_splitter.split_text(document_text)
    
    # Create or recreate collection
    try:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1536,  # OpenAI embeddings dimension
                distance=models.Distance.COSINE
            )
        )
    except Exception as e:
        print(f"Error recreating collection: {e}")
        return

    # Generate embeddings and prepare points for Qdrant
    points = []
    for i, chunk in enumerate(chunks):
        # Generate embedding
        vector = embeddings.embed_query(chunk)
        
        # Create a point for Qdrant
        point_id = str(uuid.uuid4())
        points.append(
            models.PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": chunk,
                    "chunk_id": i,
                    "source": file_path
                }
            )
        )
    
    # Upload points to Qdrant
    try:
        qdrant_client.upload_points(
            collection_name=collection_name,
            points=points,
            parallel=4  # Adjust based on your system's capabilities
        )
        print(f"Successfully uploaded {len(points)} chunks to Qdrant")
    except Exception as e:
        print(f"Error uploading to Qdrant: {e}")

# Example usage
if __name__ == "__main__":
    # Prerequisites:
    # 1. Qdrant running locally (e.g., via Docker: docker run -p 6333:6333 qdrant/qdrant)
    # 2. OpenAI API key set as environment variable or in config
    # 3. pip install langchain qdrant-client openai
    
    file_path = r"C:\Users\manjusha.pattadkal\OneDrive - XITASO GmbH\Documents\NDA.pdf"  # Replace with your document path
    process_document_to_qdrant(file_path)