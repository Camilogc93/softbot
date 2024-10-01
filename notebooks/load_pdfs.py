from langchain_community.document_loaders import PyMuPDFLoader

def load_documents(file_paths):
    """
    Loads PDF documents from a list of file paths using PyMuPDFLoader.

    Parameters:
    - file_paths: A list of file paths (strings) for the PDFs to be loaded.

    Returns:
    - documents: A list containing all loaded documents from the provided PDFs.
    """
    documents = []  # List to store all loaded documents

    for file_path in file_paths:
        loader = PyMuPDFLoader(file_path=file_path)
        docs = loader.load()  # Load documents from the current PDF
        documents.extend(docs)  # Add them to the overall documents list

    return documents
