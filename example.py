"""
Harry Potter Gen Z - Retrieval Augmented Generation (RAG) System

This script implements a RAG system for Harry Potter content with Gen Z language.
It loads documents, splits them into chunks, creates embeddings, and stores them in a vector database.
"""
import os
import shutil
from typing import List, Optional
from dotenv import load_dotenv
import time
import nltk

# Download required NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

# Langchain imports
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate

# Gemini imports
import google.generativeai as genai

# Access Google's Generative AI models,
# including the Gemini family, directly via the Gemini API or experiment rapidly using Google AI Studio.

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

# Configure Gemini API


# Constants
CHROMA_PATH = "chroma" # We are using chroma as our vector datbase
DATA_PATH = "book_1"  # Default to book_1, can be changed to "data/books" or other directories
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MODEL_NAME = "gemini-1.5-flash-latest"  # Default model
EMBEDDING_MODEL = "models/embedding-001"  # Gemini embedding model

class HarryPotterRAG:
    """RAG system for Harry Potter content"""
    print("Initializing RAG system....")
    def __init__(self, data_path: str = DATA_PATH, chroma_path: str = CHROMA_PATH):
        """Initialize the RAG system"""
        self.data_path = data_path
        self.chroma_path = chroma_path
        print(f"Embedding model: {EMBEDDING_MODEL}")
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME)
        self.vectorstore = None

    def load_documents(self) -> List[Document]:
        """Load documents from the data directory"""
        loader = DirectoryLoader(self.data_path, glob="**/*.md")
        documents = loader.load()
        print(f"Loaded {len(documents)} documents from {self.data_path}")
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks

    def create_vectorstore(self, chunks: List[Document], recreate: bool = False) -> None:
        """Create a vector store from document chunks"""
        # Clear existing database if requested
        if recreate and os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
            print(f"Removed existing database at {self.chroma_path}")

        # Create and persist the vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=self.chroma_path
        )
        self.vectorstore.persist()
        print(f"Created and persisted vector store with {len(chunks)} chunks")

    def load_vectorstore(self) -> None:
        """Load an existing vector store"""
        if not os.path.exists(self.chroma_path):
            raise ValueError(f"Vector store not found at {self.chroma_path}")

        self.vectorstore = Chroma(
            persist_directory=self.chroma_path,
            embedding_function=self.embedding_model
        )
        print(f"Loaded existing vector store from {self.chroma_path}")
        
    def create_index(self, recreate: bool = False) -> None:
        """Create the complete index pipeline"""
        documents = self.load_documents()
        chunks = self.split_documents(documents)
        self.create_vectorstore(chunks, recreate=recreate)
        print("Index creation complete!")

    def query(self, query_text: str, k: int = 3) -> dict:
        """Query the RAG system"""
        if not self.vectorstore:
            try:
                self.load_vectorstore()
            except ValueError:
                raise ValueError("Vector store not initialized. Run create_index() first.")

        # Retrieve relevant documents
        docs = self.vectorstore.similarity_search(query_text, k=k)
        context = "\n\n---\n\n".join([doc.page_content for doc in docs])

        # Create prompt
        prompt = ChatPromptTemplate.from_template("""
        You’re an assistant, I guess. Not really here to impress anyone.
        Use chill, lazy vibes — like, Gen Z slang but make it low-effort.
        If the answer’s in the context, cool. If not, don’t try too hard.
        Just do your thing. Or don’t. Whatever. make the answer at least
        200 words.
        
        {context}
        

        ---

        Question: {question}

        Answer in simple english, try to be as concise as possible, use a couple of jokes and use emojis:
        """)

        # Generate response
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "question": query_text})

        return {
            "query": query_text,
            "response": response.content,
            "source_documents": docs
        }



def main():
    """Main function to demonstrate RAG functionality"""
    print("🧙‍♂️ Harry Potter Gen Z - Retrieval Augmented Generation System 🧙‍♂️")

    # Initialize RAG system
    rag = HarryPotterRAG()

    # Create index if it doesn't exist
    if not os.path.exists(CHROMA_PATH):
        print("Creating new vector index...")
        rag.create_index()
    else:
        print("Using existing vector index...")
        rag.load_vectorstore()

    # Interactive query loop
    print("\n✨ Ready to answer your Harry Potter questions in Gen Z style! ✨")
    print("Type 'exit' to quit")

    while True:
        query = input("\nYour question: ")
        if query.lower() in ["exit", "quit", "q"]:
            break

        try:
            start_time = time.time()
            result = rag.query(query)
            end_time = time.time()

            print("\n" + "=" * 80)
            print(f"🔮 Answer (in {end_time - start_time:.2f}s):")
            print(result["response"])
            print("=" * 80)

            # Optionally show sources
            show_sources = input("\nShow sources? (y/n): ").lower() == "y"
            if show_sources:
                print("\nSources:")
                for i, doc in enumerate(result["source_documents"]):
                    print(f"\nSource {i+1}:")
                    print(f"From: {doc.metadata.get('source', 'Unknown')}")
                    print(f"Content: {doc.page_content[:200]}...")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
