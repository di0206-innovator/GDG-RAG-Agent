"""
Day 2 - Exercise 3: Vector Database Knowledge Base - HANDS-ON WORKBOOK
=======================================================================

LEARNING OBJECTIVES:
☐ Understand vector embeddings (converting text to numbers)
☐ Work with ChromaDB (a powerful vector database)
☐ Implement semantic similarity search
☐ Build a production RAG system foundation

What is a Vector Database?
===========================
Imagine a library where books aren't organized alphabetically, but by
their MEANING. Books about similar topics sit near each other, even if
their titles are completely different. That's what vector databases do!
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import uuid
import sys
import os

# Add parent dir to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)

from chunking_utility import TextChunker


class KnowledgeBase:
    """
    Your intelligent knowledge vault! 
    
    This class:
    1. Takes your documents
    2. Converts them to vector embeddings (magic numbers!)
    3. Stores them in ChromaDB
    4. Lets you search by MEANING, not just keywords
    """
    
    def __init__(self, collection_name: str = "gdg_knowledge"):
        """
        Initialize your knowledge base!
        """
        print("🚀 Initializing Knowledge Base...")
        
        # Initialize ChromaDB client (in-memory for this workshop)
        self.client = chromadb.Client()
        
        # Initialize embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        print("   Loading embedding model: all-MiniLM-L6-v2")
        print("   (This creates 384-dimensional vectors)")
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "GDG Workshop Knowledge Base"}
        )
        
        # Initialize helper utilities
        self.chunker = TextChunker(chunk_size=500, overlap=50)
        
        current_count = self.collection.count()
        
        print(f"✅ Knowledge Base '{collection_name}' ready!")
        print(f"   Current documents: {current_count} chunks")
        print()
    
    def add_document(self, text: str, metadata: Dict = None) -> List[str]:
        """
        Add a document to the knowledge base.
        """
        if metadata is None:
            metadata = {}
        
        print(f"📄 Processing document...")
        
        # Chunk the document
        chunks = self.chunker.chunk_text(text, method='sentences')
        print(f"   ✂️  Created {len(chunks)} chunks")
        
        # Prepare data for ChromaDB
        ids = []
        texts = []
        metadatas = []
        
        for chunk in chunks:
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            
            texts.append(chunk['text'])
            
            chunk_metadata = {
                **metadata,
                'chunk_id': chunk['chunk_id'],
                'word_count': chunk['word_count'],
                'method': chunk.get('method', 'unknown')
            }
            metadatas.append(chunk_metadata)
        
        # Add to ChromaDB (embeddings generated automatically!)
        print(f"   🧮 Generating embeddings...")
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        
        print(f"✅ Added {len(chunks)} chunks to knowledge base")
        print(f"   Total chunks in KB: {self.collection.count()}\n")
        
        return ids
    
    def query(self, query_text: str, top_k: int = 3) -> List[Dict]:
        """
        Search the knowledge base! 🔍
        """
        print(f"🔍 Searching for: '{query_text}'")
        print(f"   Looking for top {top_k} results...")
        
        # Query ChromaDB
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        
        # Format results nicely
        formatted_results = []
        
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i] if 'distances' in results else None
            similarity = (1 - distance) if distance is not None else None
            
            formatted_results.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': distance,
                'similarity': similarity
            })
        
        print(f"✅ Found {len(formatted_results)} relevant chunks\n")
        
        return formatted_results
    
    def get_stats(self) -> Dict:
        """
        Get statistics about your knowledge base.
        """
        return {
            'collection_name': self.collection.name,
            'total_chunks': self.collection.count(),
            'embedding_dimension': 384,
            'embedding_model': 'all-MiniLM-L6-v2'
        }
    
    def clear(self):
        """
        Clear all documents from the knowledge base.
        """
        print("⚠️  Clearing knowledge base...")
        self.client.delete_collection(self.collection.name)
        
        self.collection = self.client.create_collection(
            name=self.collection.name,
            embedding_function=self.embedding_function
        )
        
        print("✅ Knowledge base cleared (all documents removed)\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("KNOWLEDGE BASE DEMO - The Heart of RAG Systems!")
    print("=" * 70 + "\n")
    
    kb = KnowledgeBase(collection_name="gdg_demo")
    
    gdg_docs = """
    Google Developer Groups (GDG) are community groups for college and university 
    students interested in Google developer technologies. Students from all undergraduate 
    or graduate programs with an interest in growing as a developer are welcome. By 
    joining a GDG, students grow their knowledge in a peer-to-peer learning environment 
    and build solutions for local businesses and their community.
    
    Events and Activities:
    GDG chapters host various events including workshops, hackathons, study jams, and 
    tech talks. These events are designed to help students learn new technologies, 
    network with peers, and gain practical experience. Workshops typically run from 
    9:00 AM to 5:00 PM and cover topics like AI, Cloud Computing, Android Development, 
    and Web Technologies.
    
    How to Join:
    To join a GDG chapter, visit gdg.community.dev and find your local chapter. 
    Registration is free and open to all students. Once registered, you'll receive 
    notifications about upcoming events and gain access to exclusive resources and 
    learning materials.
    
    Leadership:
    Each GDG chapter is led by passionate student organizers who work closely with 
    Google Developer Experts and the broader developer community. Leaders organize 
    events, manage the community, and ensure members have a great learning experience.
    """
    
    print("=" * 70)
    print("STEP 1: Adding documents to knowledge base")
    print("=" * 70 + "\n")
    
    kb.add_document(
        gdg_docs,
        metadata={
            'source': 'GDG Guidelines',
            'type': 'official',
            'category': 'documentation'
        }
    )
    
    stats = kb.get_stats()
    print("📊 Knowledge Base Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    print("=" * 70)
    print("STEP 2: Testing semantic search")
    print("=" * 70 + "\n")
    
    test_queries = [
        "How do I join GDG?",
        "What time do workshops start?",
        "What kind of events does GDG organize?",
        "Who leads GDG chapters?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─' * 70}")
        print(f"Query {i}: '{query}'")
        print('─' * 70)
        
        results = kb.query(query, top_k=2)
        
        for j, result in enumerate(results, 1):
            similarity_pct = result['similarity'] * 100 if result['similarity'] else 0
            
            print(f"\nResult {j} (Similarity: {similarity_pct:.1f}%):")
            print(f"  Source: {result['metadata'].get('source', 'Unknown')}")
            print(f"  Text: {result['text'][:200]}...")
            
            if similarity_pct > 80:
                print(f"  Quality: 🎯 Excellent match!")
            elif similarity_pct > 60:
                print(f"  Quality: ✅ Good match")
            else:
                print(f"  Quality: 🤔 Moderate match")
    
    print("\n" + "=" * 70)
    print("CONGRATULATIONS! You've built a vector database! 🎉")
    print("=" * 70)
    print("\n📚 Key Takeaways:")
    print("   ✓ Vector embeddings capture semantic meaning")
    print("   ✓ ChromaDB enables fast similarity search")
    print("   ✓ Similarity scores tell you how relevant results are")
    print("   ✓ This is the foundation of RAG systems!")
    print()
