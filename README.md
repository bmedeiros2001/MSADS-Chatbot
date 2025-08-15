# UChicago MSADS Chatbot

A RAG-powered chatbot built to answer questions about the University of Chicago’s MS in Applied Data Science program.

## Live Demo  
[Try it here](https://msads-chatbot.streamlit.app/)

---

### Web Scraping  
- Scraped MSADS program content using `requests` + `BeautifulSoup`  
- Cleaned it up with `markdownify` because LLMs understand markdown much better than raw HTML

### Embeddings  
- Used HuggingFace model: `sentence-transformers/all-MiniLM-L6-v2`  
- Stored all content in **ChromaDB** for fast vector similarity search

### RAG Pipeline  
- Built with **LangChain’s RetrievalQA** using OpenAI’s `gpt-4o`  
- Key hyperparameters:
  - `chunk_size = 1000`, `chunk_overlap = 200`  
  - `search_type = "mmr"` with `k = 10` for diverse, relevant context retrieval  
  - Final prompt generated using LangChain Hub’s prebuilt `rag-prompt`  
  - Output includes answer + cited source URLs
