# GDG AI Workshop: Building Agents with RAG

This repository contains the complete codebase for the GDG AI Workshop series on building intelligent agents using Retrieval-Augmented Generation (RAG) techniques. The project demonstrates practical implementation of AI-powered question-answering systems with web interfaces.

## Features

- **Text Processing**: Clean and preprocess text data for better AI understanding
- **Semantic Similarity**: Calculate similarity between questions and answers using embeddings
- **FAQ Finder**: Intelligent FAQ matching system
- **Text Chunking**: Split large documents into manageable chunks for processing
- **Knowledge Base**: Vector database integration for efficient information retrieval
- **RAG Agent**: Gemini-powered conversational AI agent
- **Web Interface**: Interactive Streamlit app for user interaction
- **Web Scraping**: Extract and process content from web pages

## Project Structure

```
├── Day-1/
│   ├── faq_finder.py          # FAQ matching logic
│   ├── semantic_similarity.py # Similarity calculations
│   └── text_cleaner.py        # Text preprocessing utilities
├── Day-2/
│   ├── chunking_utility.py    # Document chunking
│   └── knowledge_base.py      # Vector database management
├── Day-3/
│   ├── gemini_wrapper.py      # Gemini AI integration
│   ├── rag_agent.py          # RAG agent implementation
│   ├── simple_rag.py         # Basic RAG example
│   ├── streamlit_app.py      # Web application
│   └── requirements.txt      # Python dependencies
├── app.py                    # Main application entry point
├── validate_workshop.py      # Validation and testing script
└── README.md                 # This file
```

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/gdg-ai-workshop.git
   cd gdg-ai-workshop
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r Day-3/requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Running the Web Application

```bash
python -m streamlit run Day-3/streamlit_app.py
```

Open your browser to `http://localhost:8501` to access the interactive web interface.

### Running Individual Components

- **Validate the setup:**
  ```bash
  python validate_workshop.py
  ```

- **Run the main app:**
  ```bash
  python app.py
  ```

## Key Components

### Day 1: Foundations
- **Text Cleaner**: Removes noise, normalizes text, handles encoding issues
- **Semantic Similarity**: Uses sentence transformers for embedding-based similarity
- **FAQ Finder**: Matches user questions to predefined FAQs

### Day 2: Data Processing
- **Chunking Utility**: Splits documents into overlapping chunks for better context
- **Knowledge Base**: Manages vector embeddings using ChromaDB

### Day 3: AI Integration
- **Gemini Wrapper**: Handles API interactions with Google's Gemini AI
- **RAG Agent**: Combines retrieval and generation for intelligent responses
- **Streamlit App**: User-friendly interface for the complete system

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Google Gemini AI**: Large language model for text generation
- **ChromaDB**: Vector database for similarity search
- **Sentence Transformers**: For text embeddings
- **BeautifulSoup**: Web scraping and HTML parsing
- **Requests**: HTTP client for API calls

## Learning Objectives

This workshop covers:
- Text preprocessing and cleaning techniques
- Vector embeddings and similarity search
- Retrieval-Augmented Generation (RAG) patterns
- API integration with modern AI models
- Building interactive web applications
- Best practices for AI application development

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is for educational purposes. Please check individual component licenses for commercial use.

## Support

For questions or issues, please open an issue on GitHub or contact the workshop organizers.