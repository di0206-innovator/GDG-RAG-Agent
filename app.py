"""
GDG AI Workshop - Complete Web Application
==========================================
An interactive web interface showcasing all the AI components built during the workshop.

Features:
- Text cleaning and preprocessing
- Semantic similarity calculations
- Intelligent FAQ matching
- Document chunking
- Vector database (Knowledge Base)
- RAG Agent with Gemini AI integration
"""

import streamlit as st
import sys
import os
import importlib.util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'Day-1'))
sys.path.insert(0, os.path.join(current_dir, 'Day-2'))
sys.path.insert(0, os.path.join(current_dir, 'Day-3'))

# Import our modules with explicit paths
try:
    from Day_1.text_cleaner import TextCleaner
    from Day_1.semantic_similarity import SemanticSimilarity
    from Day_1.faq_finder import FAQFinder
except ImportError:
    # Fallback imports
    import importlib.util
    
    spec = importlib.util.spec_from_file_location("text_cleaner", os.path.join(current_dir, 'Day-1/text_cleaner.py'))
    text_cleaner_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(text_cleaner_module)
    TextCleaner = text_cleaner_module.TextCleaner
    
    spec = importlib.util.spec_from_file_location("semantic_similarity", os.path.join(current_dir, 'Day-1/semantic_similarity.py'))
    similarity_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(similarity_module)
    SemanticSimilarity = similarity_module.SemanticSimilarity
    
    spec = importlib.util.spec_from_file_location("faq_finder", os.path.join(current_dir, 'Day-1/faq_finder.py'))
    faq_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(faq_module)
    FAQFinder = faq_module.FAQFinder

try:
    from Day_2.chunking_utility import TextChunker
except ImportError:
    spec = importlib.util.spec_from_file_location("chunking_utility", os.path.join(current_dir, 'Day-2/chunking_utility.py'))
    chunker_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chunker_module)
    TextChunker = chunker_module.TextChunker

try:
    from Day_3.gemini_wrapper import GeminiWrapper
except ImportError:
    spec = importlib.util.spec_from_file_location("gemini_wrapper", os.path.join(current_dir, 'Day-3/gemini_wrapper.py'))
    gemini_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gemini_module)
    GeminiWrapper = gemini_module.GeminiWrapper


# Set page config
st.set_page_config(
    page_title="GDG AI Workshop",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'rag_agent' not in st.session_state:
    st.session_state.rag_agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'kb' not in st.session_state:
    st.session_state.kb = None

# ============================================================================
# HEADER
# ============================================================================

st.title("🚀 GDG AI Workshop - Complete AI System")
st.markdown("""
Welcome to the **Google Developer Groups AI Workshop**! This application showcases all the components you've learned, from basic NLP utilities to a full Retrieval-Augmented Generation (RAG) system powered by Google Gemini AI.

**Built with:**
- Day 1: NLP Fundamentals (Text Cleaning, Semantic Similarity, FAQ Matching)
- Day 2: Vector Databases (Text Chunking, ChromaDB Knowledge Base)
- Day 3: AI Integration (Gemini API, RAG Agent, Web Interface)
""")

st.markdown("---")

# ============================================================================
# SIDEBAR - Setup & Configuration
# ============================================================================

with st.sidebar:
    st.header("⚙️ Setup & Configuration")
    
    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        st.success("✅ Gemini API Key detected from .env")
        show_api_section = st.checkbox("Configure API Key Manually", value=False)
    else:
        show_api_section = True
        st.warning("⚠️ No Gemini API Key found in .env")
    
    if show_api_section:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your free key from https://aistudio.google.com/app/apikey"
        )
    
    st.markdown("---")
    
    st.header("📊 About This Workshop")
    st.markdown("""
    **What You'll Learn:**
    - Text preprocessing and cleaning
    - Semantic similarity using cosine distance
    - Intelligent FAQ systems
    - Document chunking for large texts
    - Vector databases for semantic search
    - Building RAG systems with AI
    - Creating production-ready web apps
    
    **Technologies Used:**
    - Python 3.14+ / 3.11+
    - ChromaDB (Vector Database)
    - Google Gemini AI
    - Streamlit (Web Framework)
    - Sentence Transformers (Embeddings)
    """)

st.markdown("---")

# ============================================================================
# TABS - Different Sections
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 RAG Agent", 
    "🧹 Text Cleaner", 
    "📊 Semantic Similarity",
    "❓ FAQ Finder",
    "📝 Text Chunking"
])

# ============================================================================
# TAB 1: RAG AGENT (Main Feature)
# ============================================================================

with tab1:
    st.header("🤖 RAG Agent - Intelligent Q&A System")
    st.markdown("""
    This is the complete RAG (Retrieval-Augmented Generation) system!
    
    **How it works:**
    1. You ask a question
    2. The system searches the knowledge base for relevant documents
    3. Gemini generates an answer based on retrieved documents
    4. Answer includes source citations
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Initialize RAG Agent", type="primary", use_container_width=True):
            if not api_key:
                st.error("❌ Please provide a Gemini API Key!")
            else:
                with st.spinner("Initializing RAG Agent... Please wait..."):
                    try:
                        from simple_rag import SimpleRAGAgent
                        
                        # Initialize RAG agent (works without ChromaDB!)
                        agent = SimpleRAGAgent(api_key, temperature=0.3)
                        
                        # Add sample GDG data
                        gdg_data = """
                        Google Developer Groups (GDG) are community-driven groups focused on Google 
                        technologies and education. Events include workshops, hackathons, study jams, 
                        and tech talks covering topics like AI, Cloud Computing, Android, Web Development, 
                        and more.
                        
                        How to Join: Visit gdg.community.dev to find your local chapter. Registration is 
                        free and open to all students. Once registered, receive notifications about upcoming 
                        events and get access to exclusive learning resources.
                        
                        Workshop Details: Workshops typically run 9 AM - 5 PM, provide WiFi, power outlets, 
                        coffee, snacks, and lunch. Participants should bring laptops with Python 3.8+ installed.
                        
                        Topics Covered: AI fundamentals, Machine Learning, Vector Databases, RAG Systems, 
                        Cloud Computing, Android Development, Web Technologies, and more.
                        
                        Certificates: All participants who complete the workshop receive certificates 
                        acknowledging their completion and participation.
                        
                        Cost: All GDG events are completely FREE to attend! No registration fees or costs.
                        
                        Mentorship: Each workshop includes experienced mentors and Google Developer Experts
                        who are available to help answer questions and provide guidance throughout the event.
                        """
                        
                        agent.add_document(
                            gdg_data,
                            metadata={'source': 'GDG Workshop Information'}
                        )
                        
                        st.session_state.rag_agent = agent
                        
                        st.success("✅ RAG Agent initialized! You can now ask questions.")
                        st.balloons()
                    
                    except Exception as e:
                        st.error(f"❌ Error initializing RAG Agent: {str(e)}")
                        import traceback
                        st.error(f"Details: {traceback.format_exc()}")
    
    with col2:
        if st.session_state.rag_agent:
            st.success("✅ RAG Agent Ready!")
        else:
            st.info("ℹ️ Agent not initialized. Click the button to start.")
    
    st.markdown("---")
    
    # Chat interface
    if st.session_state.rag_agent:
        st.subheader("💬 Ask Questions")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # User input
        user_input = st.chat_input("Ask me anything about the workshop...")
        
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = st.session_state.rag_agent.answer(user_input, verbose=False)
                        
                        response_text = f"**Answer:** {result['answer']}\n\n"
                        
                        if result['sources']:
                            response_text += "**📚 Sources:**\n"
                            for i, source in enumerate(result['sources'], 1):
                                similarity = source['similarity'] * 100 if source['similarity'] else 0
                                response_text += f"- {source['metadata'].get('source', 'Unknown')} (Relevance: {similarity:.0f}%)\n"
                        
                        st.markdown(response_text)
                        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                    
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    else:
        st.info("⚠️ Please initialize the RAG Agent first!")

# ============================================================================
# TAB 2: TEXT CLEANER
# ============================================================================

with tab2:
    st.header("🧹 Text Cleaner - Data Preprocessing")
    st.markdown("Clean and normalize messy text data!")
    
    cleaner = TextCleaner()
    
    user_text = st.text_area(
        "Enter text to clean:",
        "  Hello, World!!!  Email: support@gdg.dev  Price: $99.99 (AMAZING Deal!!!)",
        height=150
    )
    
    if st.button("Clean Text", use_container_width=True):
        cleaned = cleaner.clean_text(user_text)
        word_count = cleaner.get_word_count(user_text)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original:")
            st.text(user_text)
        
        with col2:
            st.subheader("Cleaned:")
            st.text(cleaned)
        
        st.metric("Word Count", word_count)
        
        st.subheader("Tokenization:")
        tokens = cleaner.tokenize(user_text)
        st.write(f"Tokens: {tokens}")

# ============================================================================
# TAB 3: SEMANTIC SIMILARITY
# ============================================================================

with tab3:
    st.header("📊 Semantic Similarity - Understanding Meaning")
    st.markdown("Calculate how similar two concepts are based on their vector representations!")
    
    similarity = SemanticSimilarity()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vector 1")
        vec1_input = st.text_input(
            "Enter numbers separated by commas",
            value="0.8, 0.6, 0.2",
            key="vec1"
        )
    
    with col2:
        st.subheader("Vector 2")
        vec2_input = st.text_input(
            "Enter numbers separated by commas",
            value="0.7, 0.5, 0.3",
            key="vec2"
        )
    
    if st.button("Calculate Similarity", use_container_width=True):
        try:
            vec1 = [float(x.strip()) for x in vec1_input.split(',')]
            vec2 = [float(x.strip()) for x in vec2_input.split(',')]
            
            score = similarity.cosine_similarity(vec1, vec2)
            interpretation = similarity.interpret_similarity(score)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Similarity Score", f"{score:.3f}")
            with col2:
                st.metric("Interpretation", interpretation)
            
            # Visualization
            st.subheader("Similarity Interpretation")
            st.progress(max(0, min(1, (score + 1) / 2)))  # Normalize to 0-1
        
        except ValueError as e:
            st.error(f"❌ Invalid input: {str(e)}")

# ============================================================================
# TAB 4: FAQ FINDER
# ============================================================================

with tab4:
    st.header("❓ FAQ Finder - Intelligent Question Matching")
    st.markdown("Match user questions to similar FAQ entries using semantic similarity!")
    
    faq = FAQFinder()
    
    # Add sample FAQs
    sample_faqs = [
        ("How do I register for the event?", "Visit gdg.community.dev and click the 'Register' button."),
        ("What is the event schedule?", "The workshop runs from 9:00 AM to 5:00 PM with a lunch break."),
        ("Is there a registration fee?", "No, all GDG events are completely free to attend!"),
        ("Where is the venue located?", "The event is at Tech Hub, 123 Innovation Street, Downtown."),
        ("What should I bring?", "Bring your laptop with Python 3.8+ installed and a charger."),
    ]
    
    for question, answer in sample_faqs:
        faq.add_faq(question, answer)
    
    st.info(f"✅ Loaded {len(sample_faqs)} FAQs")
    
    user_question = st.text_input("Ask a question:")
    
    if user_question and st.button("Find Answer", use_container_width=True):
        result = faq.find_answer(user_question)
        
        st.subheader("Result:")
        st.write(f"**Question:** {user_question}")
        
        if result['matched_question']:
            st.write(f"**Matched FAQ:** {result['matched_question']}")
            st.write(f"**Confidence:** {result['confidence']:.0%}")
        
        st.info(f"**Answer:** {result['answer']}")

# ============================================================================
# TAB 5: TEXT CHUNKING
# ============================================================================

with tab5:
    st.header("📝 Text Chunking - Breaking Down Large Documents")
    st.markdown("Split large documents into manageable chunks while preserving context!")
    
    chunker = TextChunker(chunk_size=100, overlap=20)
    
    text_input = st.text_area(
        "Enter text to chunk:",
        """
        Artificial Intelligence has revolutionized technology. Machine learning algorithms process 
        vast amounts of data with incredible speed. Deep learning uses neural networks with multiple layers. 
        Natural Language Processing enables computers to understand human language. Computer vision allows 
        machines to interpret visual information. The future of AI holds immense potential for industries.
        """,
        height=200
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        chunk_size = st.slider("Chunk Size (words)", min_value=50, max_value=500, value=100, step=50)
    
    with col2:
        overlap = st.slider("Overlap (words)", min_value=0, max_value=100, value=20, step=10)
    
    if st.button("Chunk Text", use_container_width=True):
        chunker.chunk_size = chunk_size
        chunker.overlap = overlap
        
        chunks = chunker.chunk_text(text_input, method='sentences')
        stats = chunker.get_chunk_stats(chunks)
        
        st.subheader("Chunking Statistics:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Chunks", stats['total_chunks'])
        with col2:
            st.metric("Avg Words/Chunk", f"{stats['avg_words_per_chunk']:.0f}")
        with col3:
            st.metric("Min Words", stats['min_words'])
        with col4:
            st.metric("Max Words", stats['max_words'])
        
        st.subheader("Chunks Preview:")
        for i, chunk in enumerate(chunks[:5], 1):
            with st.expander(f"Chunk {i} ({chunk['word_count']} words)"):
                st.write(chunk['text'])

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎓 Built with ❤️ for the GDG AI Workshop</p>
    <p>Showcasing: NLP • Vector Databases • Generative AI • Web Development</p>
</div>
""", unsafe_allow_html=True)
