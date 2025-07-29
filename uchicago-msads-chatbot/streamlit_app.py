import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="UChicago MSADS Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from rag_functions import get_answer

# Custom CSS for University of Chicago branding
st.markdown("""
<style>
    .main-header {
        background-color: #800000;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #FFD700;
        text-align: center;
        margin: 0;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #f0f0f0;
        border-left: 4px solid #800000;
    }
    .bot-message {
        background-color: #800000;
        color: white;
    }
    .sources {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 1rem;
        border-left: 3px solid #800000;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 University of Chicago</h1>
    <p>Master's in Applied Data Science (MSADS) Program Assistant</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# OpenAI API Key (you'll set this as a secret in deployment)
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not OPENAI_API_KEY:
    st.error("⚠️ OpenAI API key not found. Please set up your API key in the deployment secrets.")
    st.stop()

# Main chat interface
st.markdown("### Ask me anything about the UChicago MSADS program!")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""s
        <div class="chat-message bot-message">
            <strong>MSADS Assistant:</strong> {message["content"]}
        </div>
        """, unsafe_allow_html=True)

        # Show sources if available
        if "sources" in message and message["sources"]:
            st.markdown("**Sources:**", unsafe_allow_html=True)
            for i, source in enumerate(message["sources"]):
                # Create clickable links
                page_name = source.split('/')[-2].replace('-', ' ').title()
                st.markdown(f'• <a href="{source}" target="_blank">{page_name}</a>', unsafe_allow_html=True)



        
# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.markdown(f"""
    <div class="chat-message user-message">
        <strong>You:</strong> {prompt}
    </div>
    """, unsafe_allow_html=True)
    
    # Get response from RAG system
    with st.spinner("Thinking..."):
        response = get_answer(prompt, OPENAI_API_KEY)
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response["answer"],
        "sources": response["sources"]
    })
    
    # Display assistant response
    st.markdown(f"""
    <div class="chat-message bot-message">
        <strong>MSADS Assistant:</strong> {response["answer"]}
    </div>
    """, unsafe_allow_html=True)
    
    # Show sources as clickable links
    if response["sources"]:
        st.markdown("**Sources:**")
        for i, source in enumerate(response["sources"], 1):
            # Extract page name from URL for cleaner display
            page_name = source.split('/')[-2].replace('-', ' ').title()
            st.markdown(f"• <a href='{source}' target='_blank'>{page_name}</a>", unsafe_allow_html=True)


# Sidebar with information
with st.sidebar:
    st.markdown("### About this Chatbot")
    st.markdown("""
    This chatbot provides information about the University of Chicago's 
    Master's in Applied Data Science (MSADS) program based on official 
    program documentation.
    
    **Features:**
    - Answers questions about admissions, curriculum, and program details
    - Provides source citations for transparency
    - Uses advanced retrieval-augmented generation (RAG) technology
    """)
    
    st.markdown("### Quick Questions to Try:")
    st.markdown("""
    - What is the tuition cost for the program?
    - What are the admission requirements?
    - How long does the program take to complete?
    - What scholarships are available?
    - Is the program STEM eligible?
    """)