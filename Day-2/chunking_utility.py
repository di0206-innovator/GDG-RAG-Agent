"""
Day 2 - Exercise 1: Text Chunking Utility - HANDS-ON WORKBOOK
==============================================================

LEARNING OBJECTIVES:
☐ Understand why chunking is critical for AI systems
☐ Implement word-based chunking with overlap
☐ Implement sentence-based chunking (better for RAG!)
☐ Build production-ready text processing tools

The Problem:
Imagine trying to remember an entire textbook at once. Impossible, right?
AI models have the same challenge! They have a "context window" - a limit
to how much text they can process at once.

The Solution: CHUNKING!
Break large documents into smaller, digestible pieces while preserving context.

Real-world example:
Instead of feeding a 100-page manual to an AI, we:
1. Break it into ~500-word chunks
2. Add overlap so context isn't lost between chunks
3. Store each chunk separately
4. Retrieve only relevant chunks when needed
"""

from typing import List, Dict
import re

class TextChunker:
    """
    An intelligent text chunking system!
    
    Think of this as a librarian who takes a huge book and divides it
    into manageable chapters, making sure each chapter makes sense on
    its own while maintaining the story flow.
    """
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize the chunker with smart defaults.
        
        Args:
            chunk_size (int): Target number of words per chunk
            overlap (int): Words to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        print(f"✨ TextChunker initialized!")
        print(f"   Chunk size: {chunk_size} words")
        print(f"   Overlap: {overlap} words")
        print(f"   Strategy: Preserve context with intelligent overlap")
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences intelligently.
        
        Args:
            text (str): Text to split
            
        Returns:
            List of sentences
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        clean_sentences = [s.strip() for s in sentences if s.strip()]
        
        return clean_sentences
    
    def count_words(self, text: str) -> int:
        """
        Count words in text.
        """
        return len(text.split())
    
    def chunk_by_words(self, text: str) -> List[Dict]:
        """
        Chunk text by word count with overlap.
        
        Strategy: Sliding window approach
        """
        words = text.split()
        chunks = []
        chunk_id = 0
        start = 0
        
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append({
                'chunk_id': chunk_id,
                'text': chunk_text,
                'start_word': start,
                'end_word': end,
                'word_count': len(chunk_words),
                'method': 'word-based'
            })
            
            chunk_id += 1
            start = end - self.overlap
            
            if start <= chunks[-1]['start_word']:
                break
        
        return chunks
    
    def chunk_by_sentences(self, text: str) -> List[Dict]:
        """
        Chunk text by sentences, respecting chunk_size limit.
        
        Strategy: Sentence-aware chunking
        """
        sentences = self.split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_word_count = 0
        chunk_id = 0
        
        for sentence in sentences:
            sentence_word_count = self.count_words(sentence)
            
            if current_word_count + sentence_word_count > self.chunk_size and current_chunk:
                chunks.append({
                    'chunk_id': chunk_id,
                    'text': ' '.join(current_chunk),
                    'sentence_count': len(current_chunk),
                    'word_count': current_word_count,
                    'method': 'sentence-based'
                })
                
                overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                current_chunk = overlap_sentences
                current_word_count = sum(self.count_words(s) for s in current_chunk)
                
                chunk_id += 1
            
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
        
        if current_chunk:
            chunks.append({
                'chunk_id': chunk_id,
                'text': ' '.join(current_chunk),
                'sentence_count': len(current_chunk),
                'word_count': current_word_count,
                'method': 'sentence-based'
            })
        
        return chunks
    
    def chunk_text(self, text: str, method: str = 'sentences') -> List[Dict]:
        """
        Main chunking method - your one-stop chunking solution!
        """
        if method == 'words':
            return self.chunk_by_words(text)
        elif method == 'sentences':
            return self.chunk_by_sentences(text)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'words' or 'sentences'")
    
    def get_chunk_stats(self, chunks: List[Dict]) -> Dict:
        """
        Get statistics about your chunks.
        """
        if not chunks:
            return {'error': 'No chunks provided'}
        
        word_counts = [chunk['word_count'] for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_words_per_chunk': sum(word_counts) / len(word_counts),
            'min_words': min(word_counts),
            'max_words': max(word_counts),
            'total_words': sum(word_counts),
            'method': chunks[0].get('method', 'unknown')
        }


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TEXT CHUNKING DEMONSTRATION - Building Blocks of RAG Systems!")
    print("=" * 70 + "\n")
    
    sample_text = """
    Artificial Intelligence has revolutionized the way we interact with technology. 
    Machine learning algorithms can now process vast amounts of data with incredible 
    speed and accuracy. These algorithms learn patterns from historical data and make 
    predictions on new, unseen data.
    
    Deep learning, a powerful subset of machine learning, uses neural networks with 
    multiple layers. These networks can automatically learn hierarchical representations 
    of data. Each layer learns increasingly complex features, from simple edges in 
    images to complete objects.
    
    Natural Language Processing is another crucial area of AI. It enables computers 
    to understand, interpret, and generate human language. Recent advances in NLP 
    have led to powerful language models like GPT and BERT. These models can perform 
    various tasks such as translation, summarization, and question answering.
    
    Computer vision is yet another fascinating field within AI. It allows machines 
    to interpret and understand visual information from the world. Applications 
    include facial recognition, object detection, and autonomous vehicles. Self-driving 
    cars use computer vision to navigate roads safely.
    
    The future of AI holds immense potential for transforming industries and improving 
    our daily lives. From healthcare diagnostics to personalized education, AI systems 
    are becoming increasingly sophisticated. However, we must also consider ethical 
    implications and ensure AI development benefits humanity as a whole.
    """
    
    print("Sample text loaded:")
    print(f"   Total words: {len(sample_text.split())}")
    print(f"   Total characters: {len(sample_text)}\n")
    
    print("-" * 70)
    print("Sentence-based chunking (RECOMMENDED)")
    print("-" * 70 + "\n")
    
    chunker = TextChunker(chunk_size=50, overlap=10)
    chunks = chunker.chunk_text(sample_text, method='sentences')
    
    print(f"✅ Created {len(chunks)} chunks\n")
    
    for i, chunk in enumerate(chunks[:3]):
        print(f"Chunk {chunk['chunk_id']} ({chunk['word_count']} words):")
        print(f"   {chunk['text'][:150]}...")
        print()
    
    stats = chunker.get_chunk_stats(chunks)
    
    print("\nChunking Statistics:")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Average words per chunk: {stats['avg_words_per_chunk']:.1f}")
    print(f"   Min/Max words: {stats['min_words']}/{stats['max_words']}")
