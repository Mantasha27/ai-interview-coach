from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def evaluate_answer(expected, student):
    """
    Evaluate student answer against expected answer using TF-IDF and Cosine Similarity
    
    Returns:
        score (float): Score out of 10
        missing (list): Missing keywords
        feedback (str): Personalized feedback
        confidence (float): Confidence score 0-100
    """
    
    # Handle empty answers
    if not student.strip():
        return 0, list(expected.split())[:5], "No answer provided", 0
    
    # TF-IDF Vectorization with bigrams for better matching
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform([expected, student])
    
    # Calculate Cosine Similarity
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    score = round(similarity * 10, 1)
    
    # Extract keywords
    expected_words = set(re.findall(r'\b\w+\b', expected.lower()))
    student_words = set(re.findall(r'\b\w+\b', student.lower()))
    
    # Find important keywords (length > 4, exclude common words)
    common_words = {'learning', 'algorithm', 'model', 'data', 'function', 'class', 'method'}
    important_keywords = [w for w in expected_words 
                         if len(w) > 4 and w not in common_words]
    missing = [w for w in important_keywords if w not in student_words]
    
    # Provide dynamic feedback based on score
    if score >= 8:
        feedback = "Excellent answer! Very relevant and well-structured. You covered all key points."
    elif score >= 6:
        feedback = "Good answer! You have the main ideas but could include more technical depth or details."
    elif score >= 4:
        feedback = "Average answer. You're on the right track but missing key concepts. Review the expected answer."
    else:
        feedback = "Answer needs improvement. Lacks relevance and conceptual clarity. Study this topic more."
    
    # Calculate confidence (0-100)
    # Based on: word count (relevance), unique words (diversity), and similarity score
    word_count = len(student.split())
    unique_words = len(set(student.split()))
    
    confidence = (word_count * 0.02) + (unique_words * 0.03) + (score * 6)
    confidence = min(round(confidence, 1), 100)  # Cap at 100%
    
    return score, missing[:5], feedback, confidence
