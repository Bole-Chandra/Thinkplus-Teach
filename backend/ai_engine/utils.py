from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def check_plagiarism(new_text, existing_texts):
    if not existing_texts:
        return 0.0
    
    documents = [new_text] + existing_texts
    tfidf_vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        return float(cosine_sim.max()) * 100  # Return percentage
    except:
        return 0.0

def generate_feedback(score, text_length):
    feedback = []
    if score > 20:
        feedback.append(f"Warning: Significant similarity detected ({score:.1f}%). Ensure proper citation.")
    else:
        feedback.append("Content originality looks good.")
    
    if text_length < 50:
        feedback.append("The submission is very short. Please provide more detail.")
    elif text_length > 1000:
        feedback.append("Good depth of content.")
    else:
        feedback.append("Adequate length.")
        
    return " ".join(feedback)
