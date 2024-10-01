
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv()
class ModelEmbedding:
    """
    A class to handle Hugging Face model embeddings.
    """

    def __init__(self, model_url="https://jy60yis5tk9j9azb.us-east-1.aws.endpoints.huggingface.cloud"):
        """
        Initializes the Hugging Face embedding model.

        """
        self.model_name = model_url
    
        # Initialize the Hugging Face embeddings
        self.hf = HuggingFaceEndpointEmbeddings(
            model=self.model_name,
            task="feature-extraction",
            huggingfacehub_api_token=os.getenv("hf_key")
        )


    def get_embeddings(self):
        """
        Returns the initialized Hugging Face embeddings instance.

        Returns:
        - hf: The Hugging Face embeddings instance.
        """
        return self.hf
