"""
Simplified RAG Agent - Works without ChromaDB
==============================================
A lightweight RAG system that doesn't require chromadb,
perfect for Streamlit web interface.
"""

import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class SimpleKnowledgeBase:
    """Simple in-memory knowledge base using semantic search"""
    
    def __init__(self):
        self.documents = []
        self.embeddings = []
    
    def add_document(self, text: str, metadata: Dict = None):
        """Add document to knowledge base"""
        if metadata is None:
            metadata = {}
        
        doc = {
            'text': text,
            'metadata': metadata,
            'id': len(self.documents)
        }
        self.documents.append(doc)
    
    def query(self, query_text: str, top_k: int = 3) -> List[Dict]:
        """Search for similar documents using keyword matching"""
        results = []
        query_words = set(query_text.lower().split())
        
        for doc in self.documents:
            doc_words = set(doc['text'].lower().split())
            
            # Calculate Jaccard similarity
            intersection = len(query_words & doc_words)
            union = len(query_words | doc_words)
            similarity = intersection / union if union > 0 else 0
            
            results.append({
                'id': doc['id'],
                'text': doc['text'],
                'metadata': doc['metadata'],
                'similarity': similarity
            })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]


class SimpleRAGAgent:
    """Simplified RAG Agent that works without ChromaDB"""
    
    def __init__(self, gemini_api_key: str, temperature: float = 0.3):
        """Initialize the RAG Agent"""
        self.api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        self.temperature = temperature
        self.kb = SimpleKnowledgeBase()
        
        # Import Gemini wrapper
        try:
            import sys
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, current_dir)
            from gemini_wrapper import GeminiWrapper
            self.llm = GeminiWrapper(api_key=self.api_key, temperature=temperature)
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini: {str(e)}")
        
        # Set persona
        self.llm.set_persona(
            "You are a helpful AI assistant with access to a knowledge base. "
            "When answering questions, you ALWAYS cite the source documents you used. "
            "If you don't find relevant information in the knowledge base, you say so honestly. "
            "You are accurate, helpful, and always provide context from the documents. "
            "You never make up information - you only use what's in the provided context."
        )
    
    def add_document(self, text: str, metadata: Dict = None):
        """Add document to knowledge base"""
        self.kb.add_document(text, metadata)
    
    def answer(self, query: str, top_k: int = 3, verbose: bool = False) -> Dict:
        """Answer a question using RAG"""
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"🔍 RAG PIPELINE STARTING")
            print(f"{'='*70}\n")
            print(f"Query: '{query}'\n")
        
        # Step 1: Retrieve context
        if verbose:
            print("Step 1/3: 🔍 Retrieving relevant context...")
        
        context_chunks = self.kb.query(query, top_k=top_k)
        
        if verbose and context_chunks:
            print(f"   ✅ Found {len(context_chunks)} relevant chunks")
            for i, chunk in enumerate(context_chunks, 1):
                similarity = chunk.get('similarity', 0) * 100
                source = chunk['metadata'].get('source', 'Unknown')
                print(f"      {i}. {source} (Similarity: {similarity:.1f}%)")
        elif verbose:
            print("   ⚠️  No relevant context found")
        
        # Step 2: Build prompt
        if verbose:
            print("\nStep 2/3: 📝 Building prompt with context...")
        
        if not context_chunks:
            prompt = f"""The user asked: "{query}"

You don't have any relevant information in your knowledge base to answer this question.
Please respond honestly that you don't have this information available."""
        else:
            context_text = "=== KNOWLEDGE BASE CONTEXT ===\n\n"
            context_text += "Here are relevant excerpts from the knowledge base:\n\n"
            
            for i, chunk in enumerate(context_chunks, 1):
                source = chunk['metadata'].get('source', 'Unknown Source')
                context_text += f"[Source {i}: {source}]\n"
                context_text += f"{chunk['text']}\n\n"
            
            prompt = f"""{context_text}
=== USER QUESTION ===

{query}

=== INSTRUCTIONS ===

Please answer the user's question using ONLY the information provided in the context above.

Important guidelines:
1. Cite which source(s) you used (e.g., "According to Source 1...", "Source 2 states...")
2. If the context contains the answer, provide it clearly and concisely
3. If the context doesn't fully answer the question, say so and explain what information is available
4. DO NOT make up information or use knowledge outside the provided context
5. Be helpful and conversational while staying factual

Your answer:"""
        
        if verbose:
            print(f"   ✅ Prompt ready")
        
        # Step 3: Generate answer
        if verbose:
            print("\nStep 3/3: 🤖 Generating answer with Gemini...")
        
        answer = self.llm.generate(prompt)
        
        if verbose:
            print(f"   ✅ Answer generated\n")
            print(f"{'='*70}\n")
        
        # Compile result
        result = {
            'query': query,
            'answer': answer,
            'sources': [
                {
                    'text': chunk['text'][:300] + '...' if len(chunk['text']) > 300 else chunk['text'],
                    'metadata': chunk['metadata'],
                    'similarity': chunk.get('similarity', 0)
                }
                for chunk in context_chunks
            ],
            'num_sources': len(context_chunks),
            'has_sources': len(context_chunks) > 0
        }
        
        return result
