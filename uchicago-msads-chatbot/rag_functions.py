__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain import hub
import streamlit as st



def format_docs(docs):
    """Format retrieved documents for the prompt"""
    return "\n\n".join(doc.page_content for doc in docs)


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
#@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(persist_directory="msads_vectorstore", embedding_function=embeddings)
vectorstore = load_vectorstore()

# print line for debugging
print("DEBUG: Your vectorstore contains", len(vectorstore.get()), "documents")


def setup_rag_chain(openai_api_key):
    """Set up the complete RAG chain - matches your exact Colab implementation"""
    try:
        print("Loading vectorstore...")
        vectorstore = load_vectorstore()
        print("Vectorstore loaded successfully")
        
        print("Initializing LLM...")
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            temperature=0
        )
        print("LLM initialized")
        
        print("Setting up retriever...")
        retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 10})
        print("Retriever set up")
        
        print("Pulling RAG prompt from hub...")
        prompt = hub.pull("rlm/rag-prompt")
        print("Prompt pulled successfully")
        
        print("Creating RAG chain...")
        rag_chain_with_sources = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        ).assign(
            answer=prompt | llm | StrOutputParser()
        )
        print("RAG chain created successfully")
        
        return rag_chain_with_sources
        
    except Exception as e:
        print(f"Error in setup_rag_chain: {e}")
        raise e   

def get_answer(question, openai_api_key):
    """Main function to get answer from RAG system - matches your exact Colab logic"""
    try:
        print(f"Question received: {question}")
        print(f"API key length: {len(openai_api_key) if openai_api_key else 'None'}")
        
        rag_chain_with_sources = setup_rag_chain(openai_api_key)
        print("RAG chain setup complete")

        # Debug: Check what documents are being retrieved
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 10})
        retrieved_docs = retriever.invoke(question)
        
        print(f"Retrieved {len(retrieved_docs)} documents:")
        for i, doc in enumerate(retrieved_docs[:3]):  # Show first 3
            print(f"Doc {i+1}: {doc.metadata.get('source', 'Unknown')}")
            print(f"Content preview: {doc.page_content[:200]}...")
            print()
        
        print("Invoking RAG chain...")
        result = rag_chain_with_sources.invoke(question)
        print("Got result from RAG chain!")


        # # Extract unique sources (exactly like your code)
        # seen = set()
        # unique_sources = []
        # for doc in result["context"]:
        #     source = doc.metadata.get("source", "Unknown")
        #     if source not in seen:
        #         seen.add(source)
        #         unique_sources.append(source)
        
        # Extract unique sources
        seen = set()
        unique_sources = []
        for doc in result["context"]:
            url = doc.metadata.get("url", "Unknown URL")
            if url not in seen:
                seen.add(url)
                unique_sources.append(url)
        
        return {
            "answer": result["answer"],
            "sources": unique_sources
        }
    except Exception as e:
        return {
            "answer": f"Sorry, I encountered an error: {str(e)}",
            "sources": []
        }