from flask import Flask, render_template, request

import os
import re
from collections import defaultdict
from math import log, exp

# Preprocessing function
def preprocess(text):
    return re.findall(r'\b\w+\b', text.lower())

# Load documents
# Load documents with UTF-8 encoding and error handling
def load_documents(folder_path):
    docs = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            try:
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8', errors='ignore') as file:
                    docs[filename] = preprocess(file.read())
            except Exception as e:
                print(f"Error reading {filename}: {e}")  
    return docs

# Compute term frequencies and document frequencies
def compute_statistics(docs):
    doc_count = len(docs)
    term_doc_freq = defaultdict(int)
    term_freq = defaultdict(lambda: defaultdict(int))

    for doc_id, words in docs.items():
        word_set = set(words)
        for word in words:
            term_freq[doc_id][word] += 1
        for word in word_set:
            term_doc_freq[word] += 1

    return term_freq, term_doc_freq, doc_count

# Compute relevance probabilities using BIM

def compute_relevance_prob(query, term_freq, term_doc_freq, doc_count):
    scores = {}
    for doc_id in term_freq:
        score = 0.0
        for term in query:
            tf = term_freq[doc_id].get(term, 0)
            df = term_doc_freq.get(term, 0)
            
            p_term_given_relevant = (tf + 1) / (sum(term_freq[doc_id].values()) + len(term_doc_freq))
            p_term_given_not_relevant = (df + 1) / (doc_count - df + len(term_doc_freq))
            
            if p_term_given_relevant > 0 and p_term_given_not_relevant > 0:
                score += log(p_term_given_relevant / p_term_given_not_relevant)
        
        # Exponentiate to bring score back from log-space
        scores[doc_id] = exp(score)
    
    return scores

# Normalize the scores to make them positive
def normalize_scores(scores):
    min_score = min(scores.values())
    normalized_scores = {doc_id: score - min_score for doc_id, score in scores.items()}
    return normalized_scores

# Main retrieval function for the web interface
def retrieve_documents(folder_path, query):
    # Load documents and preprocess query
    docs = load_documents(folder_path)
    query_terms = preprocess(query)

    # Compute term statistics
    term_freq, term_doc_freq, doc_count = compute_statistics(docs)

    # Compute relevance scores for the query
    scores = compute_relevance_prob(query_terms, term_freq, term_doc_freq, doc_count)
    
    # Rank documents based on their scores
    ranked_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    return ranked_docs  # Return ranked results to be displayed in the web app

folder_path = 'C:/Users/Envy/OneDrive/Desktop/Article'