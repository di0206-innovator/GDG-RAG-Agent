"""
Day 1 - Exercise 3: Intelligent FAQ Finder [WORKBOOK]
======================================================


The Challenge:
Users ask questions in different ways:
- "How do I sign up?" vs "How can I register?"
- "What's the cost?" vs "Do I need to pay?"

They're asking the same thing, but with different words!
Your job: Build a smart system that understands the INTENT behind questions.

What you'll learn:
✓ Combining text cleaning + similarity matching
✓ Building a simple knowledge base
✓ Handling word synonyms
✓ Creating your first intelligent system!

Real-world use:
This is how chatbots, help centers, and support systems work!

INSTRUCTIONS:
Look for TODO comments and fill in the missing code!
"""

import importlib
from typing import List, Dict

# Import our previous utilities
from text_cleaner import TextCleaner
from semantic_similarity import SemanticSimilarity


class FAQFinder:
    """
    An intelligent FAQ matching system! 🤖
    
    Think of this as a smart librarian who understands what you're
    asking for, even if you don't use the exact words from the book titles.
    
    How it works:
    1. Store FAQ questions and answers
    2. When user asks a question, clean it up
    3. Find the most similar FAQ question
    4. Return that answer!
    """
    
    def __init__(self):
        """
        Initialize our FAQ finder with helpful tools.
        
        We're using:
        - TextCleaner: To clean messy input
        - SemanticSimilarity: To find matches (we'll keep this for structure)
        - Stop words: Common words like "the", "is", "a" that don't add meaning
        - Synonyms: Different words with same meaning (e.g., "sign" = "register")
        """
        # TODO: Initialize TextCleaner
        # Hint: self.cleaner = TextCleaner()
        self.cleaner = TextCleaner()
        
        # TODO: Initialize SemanticSimilarity
        # Hint: self.similarity = SemanticSimilarity()
        self.similarity = SemanticSimilarity()
        
        # TODO: Initialize empty list for FAQs
        self.faqs = []
        
        # Words to ignore (they don't help us match questions)
        self.stop_words = {
            'a', 'an', 'the', 'is', 'are', 'am', 'be', 'to', 'of', 'in', 
            'on', 'at', 'for', 'with', 'do', 'does', 'i', 'you', 'we', 
            'they', 'there', 'can', 'will', 'it', 'what', 'how', 'when', 'where'
        }
        
        # Words that mean the same thing (helps with matching!)
        self.synonyms = {
            'sign': ['register', 'signup', 'join', 'enroll'],
            'register': ['sign', 'signup', 'join', 'enroll'],
            'signup': ['sign', 'register', 'join', 'enroll'],
            'pay': ['fee', 'cost', 'price', 'money', 'charge'],
            'fee': ['pay', 'cost', 'price', 'money', 'charge'],
            'cost': ['pay', 'fee', 'price', 'money', 'charge'],
            'start': ['schedule', 'time', 'begin', 'when'],
            'time': ['schedule', 'start', 'when'],
            'when': ['time', 'schedule', 'start'],
            'where': ['venue', 'location', 'place'],
            'venue': ['where', 'location', 'place'],
            'location': ['where', 'venue', 'place']
        }
        
        print("[OK] FAQ Finder initialized with smart matching!")
    
    def add_faq(self, question: str, answer: str):
        """
        Add a question-answer pair to our knowledge base.
        
        Args:
            question (str): The FAQ question
            answer (str): The answer to return
        
        Example:
            >>> finder.add_faq(
            ...     "How do I register?",
            ...     "Visit gdg.community.dev and click Register"
            ... )
        """
        # TODO: Append a dictionary to self.faqs with the question, answer, 
        # and cleaned question
        # Hint: Use self.cleaner.clean_text(question) for the clean version
        self.faqs.append({
            'question': question,
            'answer': answer,
            'question_clean': self.cleaner.clean_text(question)
        })
    
    def load_from_file(self, filepath: str):
        """
        Load FAQs from a file.
        
        Expected format (pipe-separated):
        Question|Answer
        How do I register?|Visit our website...
        
        This makes it easy to manage lots of FAQs!
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and '|' in line:
                        question, answer = line.split('|', 1)
                        self.add_faq(question.strip(), answer.strip())
            
            print(f"✅ Loaded {len(self.faqs)} FAQs from {filepath}")
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def expand_with_synonyms(self, words: set) -> set:
        """
        Expand a set of words with their synonyms.
        
        Example: {"sign"} → {"sign", "register", "signup", "join", "enroll"}
        
        This helps us match questions even when different words are used!
        """
        # TODO: Create a copy of words set
        expanded = set(words)
        
        # TODO: Loop through words and add synonyms
        for word in words:
            # TODO: Check if word has synonyms in self.synonyms
            if word in self.synonyms:
                expanded.update(self.synonyms[word])
        
        return expanded
    
    def find_answer(self, user_question: str, threshold: float = 0.15) -> Dict:
        """
        Find the best matching answer for a user's question! 🎯
        
        The Process:
        1. Clean the user's question
        2. Remove stop words (keep only meaningful words)
        3. Expand with synonyms
        4. Compare against all FAQ questions
        5. Return the best match (if above threshold)
        
        Args:
            user_question (str): What the user is asking
            threshold (float): Minimum similarity score (0-1) to return answer
        
        Returns:
            dict: Contains 'answer', 'confidence', and 'matched_question'
        
        Example:
            >>> result = finder.find_answer("How can I sign up?")
            >>> print(result['answer'])
            "Visit gdg.community.dev and click Register"
        """
        if not self.faqs:
            return {
                'answer': "❌ No FAQs loaded yet! Please add some FAQs first.",
                'confidence': 0.0,
                'matched_question': None
            }
        
        # TODO: Step 1 & 2 - Clean and tokenize user question
        # Hint: Use self.cleaner.clean_text(user_question)
        user_clean = self.cleaner.clean_text(user_question)
        
        # TODO: Split into words and remove stop words
        # Hint: set(user_clean.split()) - self.stop_words
        user_words_raw = set(user_clean.split()) - self.stop_words
        
        # TODO: Step 3 - Expand with synonyms
        # Hint: Use self.expand_with_synonyms(user_words_raw)
        user_words = self.expand_with_synonyms(user_words_raw)
        
        # Handle case where all words were stop words
        if not user_words:
            user_words = set(user_clean.split())
        
        # Step 4: Find best matching FAQ
        best_match = None
        best_score = 0.0
        
        # TODO: Loop through all FAQs to find best match
        for faq in self.faqs:
            # TODO: Process FAQ question same way as user question
            # Remove stop words from FAQ
            faq_words_raw = set(faq['question_clean'].split()) - self.stop_words
            
            # TODO: Expand FAQ words with synonyms
            faq_words = self.expand_with_synonyms(faq_words_raw)
            
            if not faq_words:
                faq_words = set(faq['question_clean'].split())
            
            # TODO: Calculate Jaccard similarity (overlap / union)
            # This tells us: "How many words do they have in common?"
            
            # TODO: Find intersection (common words)
            # Hint: user_words.intersection(faq_words)
            intersection = user_words.intersection(faq_words)
            
            # TODO: Find union (all unique words from both)
            # Hint: user_words.union(faq_words)
            union = user_words.union(faq_words)
            
            # TODO: Calculate score
            if len(union) > 0:
                score = len(intersection) / len(union)
            else:
                score = 0.0
            
            # Keep track of best match
            if score > best_score:
                best_score = score
                best_match = faq
        
        # Step 5: Return result (if confident enough)
        if best_score < threshold:
            return {
                'answer': "I couldn't find a good answer to that question. Could you rephrase it?",
                'confidence': best_score,
                'matched_question': None
            }
        
        return {
            'answer': best_match['answer'],
            'confidence': best_score,
            'matched_question': best_match['question']
        }


# ============================================================================
# DEMO: Let's build an intelligent FAQ system! 🚀
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("INTELLIGENT FAQ FINDER DEMO - Your First AI Application!")
    print("=" * 70 + "\n")
    
    # Create our finder
    finder = FAQFinder()
    
    # Sample GDG event FAQs
    print("[DATA] Loading GDG Event FAQs...\n")
    
    gdg_faqs = [
        {
            'question': "How do I register for the event?",
            'answer': "Visit our website at gdg.community.dev and click the 'Register' button on the event page."
        },
        {
            'question': "What is the event schedule?",
            'answer': "The workshop runs from 2:00 PM to 5:00 PM with lunch break in between."
        },
        {
            'question': "Where is the venue located?",
            'answer': "The event is at Tech Hub Innovation Center, 123 Innovation Street, Downtown."
        },
        {
            'question': "Is there a registration fee?",
            'answer': "No, all GDG events are completely free to attend!"
        },
        {
            'question': "What should I bring to the workshop?",
            'answer': "Bring your laptop with Python 3.8+ installed, a charger, and enthusiasm to learn!"
        },
        {
            'question': "Can beginners attend?",
            'answer': "Absolutely! Our workshops are designed for all skill levels, from beginners to advanced."
        },
        {
            'question': "Will there be food?",
            'answer': "Yes! We provide coffee, snacks throughout the day, and lunch."
        },
        {
            'question': "What technologies will be covered?",
            'answer': "We'll cover Python, AI fundamentals, vector databases, RAG systems, and LLM integration."
        }
    ]
    
    for faq in gdg_faqs:
        finder.add_faq(faq['question'], faq['answer'])
    
    print(f"[OK] Loaded {len(gdg_faqs)} FAQs into the system\n")
    
    print("-" * 70)
    print("[TEST] Let's try different ways of asking the same questions!")
    print("-" * 70 + "\n")
    
    # Test queries - notice how they use different wording!
    test_queries = [
        ("How can I sign up?", "Original: 'How do I register?'"),
        ("What time does it start?", "Original: 'What is the event schedule?'"),
        ("Do I need to pay anything?", "Original: 'Is there a registration fee?'"),
        ("Where is it happening?", "Original: 'Where is the venue?'"),
        ("What do I need to bring?", "Original: 'What should I bring?'"),
    ]
    
    for query, hint in test_queries:
        result = finder.find_answer(query)
        
        print(f"User asks: \"{query}\"")
        print(f"  Matched: {result['matched_question']}")
        print(f"  Confidence: {result['confidence']:.0%} {'[✓]' if result['confidence'] > 0.5 else '[OK]'}")
        print(f"  Answer: {result['answer']}")
        print(f"  Hint: {hint}")
        print()
    
    print("-" * 70)
    print("[TEST] What happens with unrelated questions?")
    print("-" * 70 + "\n")
    
    unrelated = [
        "What's the weather like?",
        "Who won the game yesterday?",
    ]
    
    for query in unrelated:
        result = finder.find_answer(query)
        print(f"User asks: \"{query}\"")
        print(f"  Confidence: {result['confidence']:.0%}")
        print(f"  Answer: {result['answer']}")
        print()