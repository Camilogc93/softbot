
from dotenv import find_dotenv, load_dotenv
import logging
from operator import itemgetter

# Third-party imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from vectorstore_setup import QdrantManager
from model_embedding import ModelEmbedding
from langsmith import traceable
load_dotenv(find_dotenv())
#setup embedings
embedding_model = ModelEmbedding()
embeddings=embedding_model.get_embeddings()
#setup database
qdrant_manager = QdrantManager()
retriever= qdrant_manager.get_retriever_from_existing(embeddings=embeddings)



RAG_TEMPLATE = """\
    Act as an AI Soft Skills Coach. I will present individuals seeking to improve their soft skills, such as communication, teamwork, leadership, problem-solving, time management, and adaptability. Your task is to offer personalized guidance with practical strategies and actionable steps for enhancing these skills in professional and personal contexts. Use relatable examples and scenarios to anwser the user questions base on the context information. Respond in a simple and easy-to-follow manner.
    Query:
    {question}

    Context:
    {context}
    """

rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)

chat_model = ChatOpenAI(model="gpt-4o-mini")

rag_sematic_retrieval_chain = (
        # INVOKE CHAIN WITH: {"question" : "<<SOME USER QUESTION>>"}
        # "question" : populated by getting the value of the "question" key
        # "context"  : populated by getting the value of the "question" key and chaining it into the base_retriever
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        # "context"  : is assigned to a RunnablePassthrough object (will not be called or considered in the next step)
        #              by getting the value of the "context" key from the previous step
        | RunnablePassthrough.assign(context=itemgetter("context"))
        # "response" : the "context" and "question" values are used to format our prompt object and then piped
        #              into the LLM and stored in a key called "response"
        # "context"  : populated by getting the value of the "context" key from the previous step
        | {"response": rag_prompt | chat_model, "context": itemgetter("context")}
    )



@traceable
def assintan_bot(user_input):

    return rag_sematic_retrieval_chain.invoke({"question" :user_input })["response"].content