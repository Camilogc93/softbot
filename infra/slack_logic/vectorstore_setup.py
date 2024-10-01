import os
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client import QdrantClient, models
import qdrant_client
from langchain_qdrant import QdrantVectorStore
from dotenv import find_dotenv, load_dotenv

load_dotenv()
#print(os.getenv("quadran_key"))

class QdrantManager:
    def __init__(self, collection_name='soft_collection', vector_size=1024, distance=Distance.COSINE, api_key=None, endpoint=None):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance
        self.api_key =os.getenv("quadran_key")
        self.endpoint =os.getenv("endpoint")
        self.client = self._connect_client()

    def _connect_client(self):
        """Initialize the Qdrant client connection."""
        return QdrantClient(
            url=self.endpoint,
            api_key=self.api_key,
            https=True,
            port=6333  # For Qdrant Cloud, None for local instance
        )

    def create_collection(self):
        """Create a collection in Qdrant."""
        vectors_config = VectorParams(size=self.vector_size, distance=self.distance)
        optimizers_config = models.OptimizersConfigDiff(indexing_threshold=0)
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=vectors_config,
            optimizers_config=optimizers_config
        )
        print(f"Collection '{self.collection_name}' created successfully.")

    def load_documents(self, rag_documents, embeddings):
        """Load documents into Qdrant."""
        qdrant = QdrantVectorStore.from_documents(
            rag_documents,
            embeddings,
            url=self.endpoint,
            prefer_grpc=True,
            api_key=self.api_key,
            collection_name=self.collection_name
        )
        return qdrant

    def get_retriever(self, rag_documents, embeddings):
        """Retrieve the Qdrant retriever."""
        qdrant = self.load_documents(rag_documents, embeddings)
        retriever = qdrant.as_retriever()
        return retriever
    

    def get_retriever_from_existing(self, embeddings):
        """Get a retriever from an existing collection without loading new documents."""
        qdrant = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name=self.collection_name,
            url=self.endpoint,
            api_key=self.api_key
        )
        retriever = qdrant.as_retriever()
        return retriever
