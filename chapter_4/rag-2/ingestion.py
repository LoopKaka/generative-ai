from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

# 1. Ingestion
#     Pdf load
file_path = "python.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()


#     Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=500
)

splited_docs=text_splitter.split_documents(docs)

#     Vector Embaddings
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

#     Store In Vector DB (Qdrant DB) - "splited_docs" convert to vectore embadding using "embeddings_model"
vectore_store = QdrantVectorStore.from_documents(
    url="http://localhost:6333",
    collection_name="genai",
    embedding=embeddings_model,
    documents=splited_docs
)

print("Ingestion is completed")