"""
Day 3 - Exercise 3: Streamlit Web Interface - WORKBOOK 🎓

Fill in every blank marked  ___  to complete the code.
Run with:  streamlit run streamlit_app_workbook.py

HOW TO USE THIS WORKBOOK
-------------------------
  • Find every  ___  and replace it with the correct value
  • The  # ✏️ FILL IN  comment tells you exactly what to write
  • The  # 💡 HINT  comment gives extra guidance
-------------------------

What is Streamlit?
Streamlit is a Python library that turns your code into beautiful,
interactive web apps in minutes - no HTML, CSS, or JavaScript needed!

Think of it as: "Python scripts → Beautiful web apps"

Why Streamlit for AI apps?
Dead simple to use
Perfect for data science and ML demos
Real-time interactivity
Free hosting available
Looks professional out of the box

What you'll learn:
✓ Building web UIs with Streamlit
✓ Chat interfaces
✓ File uploads
✓ Session state management
✓ Deploying AI applications

Real-world use:
This is how many AI startups build their MVPs!
"""

import streamlit as st
import sys
import os
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# Add project root to sys.path so package imports like DAY_2.knowledge_base work
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try standard package imports first; fallback to direct module import if needed
try:
    from Day_3.rag_agent import RAGAgent
    from Day_2.knowledge_base import KnowledgeBase
except Exception:
    # Fallback for environments running the file directly where packages aren't resolved
    sys.path.insert(0, os.path.join(project_root, 'Day-2'))
    sys.path.insert(0, os.path.join(project_root, 'Day-3'))
    from rag_agent import RAGAgent
    from knowledge_base import KnowledgeBase


def init_session_state():
    """
    Initialize Streamlit session state.
    
    Session state = variables that persist across page reloads.
    Think of it as the app's memory!
    
    We track:
    - RAG agent instance
    - Chat message history
    - Knowledge base instance
    """
    # Initialize core app state
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'kb' not in st.session_state:
        st.session_state.kb = None
    if 'auto_initialized' not in st.session_state:
        st.session_state.auto_initialized = False


def main():
    """
    Main application function.
    
    This is where we build our beautiful web interface!
    """
    
    # Configure the page
    st.set_page_config(
        page_title="GDG Knowledge Agent",
        page_icon="https://res.cloudinary.com/startup-grind/image/upload/c_fill,dpr_2.0,f_auto,g_center,h_1200,q_100,w_1200/v1/gcs/platform-data-goog/contentbuilder/GDG_Bevy_SocialSharingThumbnail_KFxxrrs.png",
        layout="wide",  # Use full screen width
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Auto-initialize if API key is in environment and not already initialized
    env_api_key = os.getenv('GEMINI_API_KEY')
    if env_api_key and not st.session_state.auto_initialized and st.session_state.agent is None:
        try:
            # Create knowledge base with new collection name
            st.session_state.kb = KnowledgeBase("gdg_knowledge_v2")
            
            # Load GDG guidelines from file
            guidelines_path = os.path.join(project_root, 'Day-2', 'data', 'gdg_guidelines.txt')
            if os.path.exists(guidelines_path):
                with open(guidelines_path, 'r', encoding='utf-8') as f:
                    guidelines_data = f.read()
                
                st.session_state.kb.add_document(
                    guidelines_data,
                    metadata={'source': 'GDG Guidelines', 'type': 'official', 'filename': 'gdg_guidelines.txt'}
                )
            
            # Initialize RAG agent (will use env variable)
            st.session_state.agent = RAGAgent(
                gemini_api_key=env_api_key,
                knowledge_base=st.session_state.kb,
            )
            
            st.session_state.auto_initialized = True
            
        except Exception as e:
            # Silently fail on auto-init, user can try manually
            pass
    
    # =================================================================
    # HEADER
    # =================================================================
    
    st.title("GDG Knowledge Agent")
    st.markdown("*Powered by Retrieval-Augmented Generation (RAG) with Gemini AI*")
    
    st.markdown("---")
    
    # =================================================================
    # SIDEBAR - Configuration & Setup
    # =================================================================
    
    with st.sidebar:
        # Check for API key in environment
        env_api_key = os.getenv('GEMINI_API_KEY')
        
        # Only show Configuration section if NO environment API key
        if not env_api_key:
            st.header("⚙️ Configuration")
            
            # API Key input
            # ✏️ FILL IN: Replace ___ with "password" to hide the key while typing
            # 💡 HINT: type="password"
            api_key = st.text_input(
                "Gemini API Key",
                type="password",
                help="Get your free key from https://aistudio.google.com/app/apikey",
                placeholder="Enter your API key here..."
            )
            
            with st.expander("💡 API Key Tips"):
                st.markdown("""
                **Getting an API Key:**
                1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
                2. Sign in with your Google account
                3. Click "Get API Key" or "Create API Key"
                4. Copy the key and paste it above
                
                **Free Tier Limits:**
                - 15 requests per minute
                - 1,500 requests per day
                - If you hit limits, wait 60 seconds or use a new key
                
                **If You Change Keys:**
                - Click "🔄 Reset Knowledge Base" below
                - Re-initialize the agent with the new key
                """)
            
            # Initialize button
            if st.button("🚀 Initialize Agent", type="primary", use_container_width=True):
                if not api_key:
                    st.error("⚠️ Please provide your Gemini API key or set GEMINI_API_KEY environment variable!")
                else:
                    with st.spinner("Initializing RAG Agent... This may take a moment..."):
                        try:
                            # Create knowledge base with new collection name
                            st.session_state.kb = KnowledgeBase("gdg_knowledge_v2")
                            
                            # Load GDG guidelines from file
                            guidelines_path = os.path.join(project_root, 'Day-2', 'data', 'gdg_guidelines.txt')
                            if os.path.exists(guidelines_path):
                                with open(guidelines_path, 'r', encoding='utf-8') as f:
                                    guidelines_data = f.read()
                                
                                st.session_state.kb.add_document(
                                    guidelines_data,
                                    metadata={'source': 'GDG Guidelines', 'type': 'official', 'filename': 'gdg_guidelines.txt'}
                                )
                            
                            # Initialize RAG agent
                            st.session_state.agent = RAGAgent(
                                gemini_api_key=api_key,
                                knowledge_base=st.session_state.kb,
                            )
                            
                            st.success("✅ Agent initialized successfully with GDG Guidelines!")
                            st.balloons()  # Celebration! 🎉
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            st.markdown("---")
        
        # Document upload section
        st.header("📄 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Upload documents to expand knowledge base",
            accept_multiple_files=True,
            type=['txt', 'md'],
            help="Upload .txt or .md files containing information you want the agent to learn"
        )
        
        if uploaded_files and st.button("Process Documents", use_container_width=True):
            if st.session_state.kb is None:
                st.error("⚠️ Please initialize the agent first!")
            else:
                with st.spinner(f"Processing {len(uploaded_files)} files..."):
                    try:
                        for file in uploaded_files:
                            file_ext = Path(file.name).suffix.lower()
                            
                            # Read text file content
                            text = file.read().decode('utf-8')
                            
                            # Add to knowledge base
                            st.session_state.kb.add_document(
                                text,
                                metadata={'source': file.name, 'type': 'user-uploaded', 'file_type': file_ext}
                            )
                        
                        st.success(f"✅ Processed {len(uploaded_files)} documents successfully!")
                    
                    except Exception as e:
                        st.error(f"❌ Error processing files: {str(e)}")
        
        st.markdown("---")
        
        # Web scraping section
        st.header("🌐 Fetch Live Data")
        
        gdg_url = st.text_input(
            "GDG Chapter URL",
            placeholder="https://gdg.community.dev/your-chapter/",
            help="Enter a GDG chapter page URL to fetch latest events and information"
        )
        
        if st.button("Fetch Latest Events", use_container_width=True):
            if st.session_state.kb is None:
                st.error("⚠️ Please initialize the agent first!")
            elif not gdg_url:
                st.warning("⚠️ Please enter a GDG chapter URL!")
            else:
                with st.spinner(f"Fetching data from {gdg_url}..."):
                    try:
                        # Fetch webpage content
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                        response = requests.get(gdg_url, headers=headers, timeout=10)
                        response.raise_for_status()
                        
                        # Parse with BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Extract text content
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Get text
                        text = soup.get_text()
                        
                        # Clean up whitespace
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = '\n'.join(chunk for chunk in chunks if chunk)
                        
                        # Add to knowledge base
                        # ✏️ FILL IN: Replace ___ with the URL variable gdg_url
                        # 💡 HINT: 'source': gdg_url
                        st.session_state.kb.add_document(
                            text,
                            metadata={
                                'source': gdg_url,
                                'type': 'web-scraped',
                                'fetched_at': datetime.utcnow().isoformat() + 'Z'
                            }
                        )
                        
                        st.success(f"✅ Successfully fetched and processed data from GDG page!")
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error fetching webpage: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Error processing webpage: {str(e)}")
        
        st.markdown("---")
        
        # Statistics section
        if st.session_state.kb:
            st.header("📊 Knowledge Base Stats")
            stats = st.session_state.kb.get_stats()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Chunks", stats['total_chunks'])
            
            with col2:
                st.metric("Embedding Dim", stats['embedding_dimension'])
            
            st.caption(f"Model: {stats['embedding_model']}")
            
            # Reset button
            if st.button("🔄 Reset Knowledge Base", use_container_width=True, type="secondary"):
                st.session_state.agent = None
                st.session_state.kb = None
                st.session_state.messages = []
                st.session_state.auto_initialized = False
                env_api_key = os.getenv('GEMINI_API_KEY')
                if env_api_key:
                    st.success("✅ Knowledge base reset! Refresh the page to reinitialize.")
                else:
                    st.success("✅ Knowledge base reset! Click 'Initialize Agent' to start fresh.")
                st.rerun()
        
        st.markdown("---")
        
        # Help section
        with st.expander("How to Use"):
            env_api_key = os.getenv('GEMINI_API_KEY')
            
            if env_api_key:
                # Simplified help for auto-initialized apps
                st.markdown("""
                **Getting Started:**
                ✅ Agent is ready! Just start asking questions below.
                
                **Knowledge Sources:**
                - **Built-in:** GDG Guidelines automatically loaded
                - **Upload PDFs:** Add your own PDF documents
                - **Upload Text:** Add .txt or .md files
                - **Live Data:** Fetch latest info from GDG chapter pages
                
                **Tips:**
                - Be specific in your questions
                - Upload relevant documents for better answers
                - Check sources to verify information
                - Use web scraping to get latest event info
                
                **Example Questions:**
                - How do I register for GDG events?
                - What's the event schedule?
                - Is there a fee for workshops?
                - What are the code of conduct guidelines?
                - When is the next DevFest?
                """)
            else:
                # Full help with setup instructions
                st.markdown("""
                **Getting Started:**
                1. Enter your Gemini API key above
                2. Click "Initialize Agent"
                3. Start asking questions!
                
                **Knowledge Sources:**
                - **Built-in:** GDG Guidelines automatically loaded
                - **Upload PDFs:** Add your own PDF documents
                - **Upload Text:** Add .txt or .md files
                - **Live Data:** Fetch latest info from GDG chapter pages
                
                **Tips:**
                - Be specific in your questions
                - Upload relevant documents for better answers
                - Check sources to verify information
                - Use web scraping to get latest event info
                
                **Example Questions:**
                - How do I register for GDG events?
                - What's the event schedule?
                - Is there a fee for workshops?
                - What are the code of conduct guidelines?
                - When is the next DevFest?
                """)
    
    # =================================================================
    # MAIN AREA - Chat Interface
    # =================================================================
    
    if st.session_state.agent is None:
        # Show welcome screen before initialization
        env_api_key = os.getenv('GEMINI_API_KEY')
        
        if env_api_key:
            # If env key exists but agent not initialized, show loading state
            st.info("🔄 Initializing agent... Please wait or refresh the page.")
        else:
            # No env key, user needs to configure manually
            st.info("👈 Please configure and initialize the agent in the sidebar to begin")
            st.markdown("## Ask Questions about GDG here once the agent is ready!")
        
    else:
        # Chat interface
        st.header("💬 Ask Me Anything!")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources for assistant messages
                if message["role"] == "assistant" and "sources" in message:
                    if message["sources"]:
                        with st.expander(f"📚 View {len(message['sources'])} Sources"):
                            for i, source in enumerate(message['sources'], 1):
                                similarity = source.get('similarity', 0) * 100
                                
                                st.markdown(f"**Source {i}:** {source['metadata'].get('source', 'Unknown')}")
                                st.caption(f"Relevance: {similarity:.1f}%")
                                st.text(source['text'][:200] + "...")
                                st.markdown("---")
        
        # Chat input
        if prompt := st.chat_input("Ask about GDG events, workshops, or anything in the knowledge base..."):
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        # Get RAG response
                        result = st.session_state.agent.answer(prompt, verbose=False)
                        st.markdown(result['answer'])
                        
                        # Display sources
                        if result['sources']:
                            with st.expander(f"📚 View {len(result['sources'])} Sources"):
                                for i, source in enumerate(result['sources'], 1):
                                    similarity = source.get('similarity', 0) * 100
                                    
                                    st.markdown(f"**Source {i}:** {source['metadata'].get('source', 'Unknown')}")
                                    st.caption(f"Relevance: {similarity:.1f}%")
                                    st.text(source['text'][:200] + "...")
                                    st.markdown("---")
                        else:
                            st.caption("No sources found in knowledge base")
                        
                        # Add assistant message to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result['answer'],
                            "sources": result['sources']
                        })
                        
                    except Exception as e:
                        error_message = str(e)
                        
                        # Check if it's a quota error
                        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message or "quota" in error_message.lower():
                            st.error("""
                            ⚠️ **API Quota Exceeded**
                            
                            You've hit the Gemini API free tier limit (15-20 requests per minute).
                            
                            **Solutions:**
                            1. **Wait 60 seconds** and try again
                            2. **Use a different API key** (get one at https://aistudio.google.com/app/apikey)
                            3. **Upgrade your API plan** for higher quotas
                            4. **Restart the app** after changing API key
                            
                            To restart with a new key:
                            - Click "🔄 Reset Knowledge Base" in the sidebar
                            - Enter your new API key
                            - Click "Initialize Agent"
                            """)
                        else:
                            st.error(f"❌ Error: {error_message}")
                        
                        # Add error to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "Sorry, I encountered an error. Please try again or check the error message above.",
                            "sources": []
                        })
        
        # Clear chat button
        if st.session_state.messages:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.messages = []
                st.rerun()


# =================================================================
# RUN THE APP
# =================================================================

if __name__ == "__main__":
    main()