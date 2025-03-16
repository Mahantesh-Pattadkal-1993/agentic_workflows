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

import uuid
from qdrant_client import QdrantClient
from qdrant_client import models




class QdrantDB:
    _instance = None

    def __new__(cls):
        """Create a single instance of QdrantManager (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(QdrantDB, cls).__new__(cls)
            # Initialize attributes only once when the instance is first created

    
            cls._instance.client = QdrantClient(qdrant_url="localhost", port=6333)
            cls._instance.collection_name = "mantumanju"
            cls._instance.embedding_model = OpenAIEmbeddings()
        return cls._instance

    def check_and_create_collection(self, vector_size=1536, distance=models.Distance.COSINE):
        """Check if collection exists; create it if it doesn’t."""
        try:
            collections = self.client.get_collections().collections
            collection_exists = any(col.name == self.collection_name for col in collections)

            if not collection_exists:
                self.client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=distance
                    )
                )
                print(f"Created collection: {self.collection_name}")
            else:
                print(f"Collection {self.collection_name} already exists")
        except Exception as e:
            print(f"Error checking/creating collection: {e}")
            raise
    

    def upsert_chunks(self, chunks:list):
        """Add points (embeddings) to the Qdrant collection."""
        
    # Generate embeddings and prepare points for Qdrant
        points = []
        for i, chunk in enumerate(chunks):
            # Generate embedding
            vector = self.embedding_model.embed_query(chunk)
            
            # Create a point for Qdrant
            point_id = str(uuid.uuid4())
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "text": chunk,
                        "chunk_id": i,
                        #"source": file_path
                    }
                )
            )
    
        self.check_and_create_collection()
        self.client.upload_points(collection_name=self.collection_name,
            points=points,
            parallel=4
                )

    def delete_points(self, point_ids):
        """Delete points from the Qdrant collection by their IDs."""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=point_ids
                )
            )
            print(f"Successfully deleted {len(point_ids)} points from Qdrant")
        except Exception as e:
            print(f"Error deleting points from Qdrant: {e}")
            raise



# Example usage
if __name__ == "__main__":
    # Prerequisites:
    # 1. Qdrant running locally (e.g., docker run -p 6333:6333 qdrant/qdrant)
    # 2. pip install qdrant-client langchain openai python-dotenv
    # 3. OpenAI API key in .env

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    # Mock read_document function
    def read_document(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # Initialize dependencies
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embeddings = OpenAIEmbeddings()

    # Create singleton instances (they’ll point to the same object)
    qdrant1 = QdrantDB(qdrant_url="localhost", qdrant_port=6333, collection_name="my_collection")
    qdrant2 = QdrantDB(qdrant_url="different-url", qdrant_port=9999, collection_name="other_collection")

    # Prove it’s a singleton (qdrant1 and qdrant2 are the same instance)
    print(f"qdrant1 is qdrant2: {qdrant1 is qdrant2}")  # True
    print(f"qdrant1 collection: {qdrant1.collection_name}")  # my_collection
    print(f"qdrant2 collection: {qdrant2.collection_name}")  # my_collection (not other_collection)

    # Process a document
    file_path = r"C:\Users\manjusha.pattadkal\OneDrive - XITASO GmbH\Documents\NDA.pdf"
    qdrant1.process_document(file_path, text_splitter, embeddings, read_document)

    # Example: Delete points
    sample_point_ids = ["some-uuid-here"]
    qdrant1.delete_points(sample_point_ids)
