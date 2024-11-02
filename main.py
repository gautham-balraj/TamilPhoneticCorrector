import csv
from typing import List, Dict
import Levenshtein
import difflib
import time
import re

def load_dictionary(file_path: str) -> Dict[str, bool]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return {line.strip().lower(): True for line in f}

def load_phrases(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

def preprocess_word(word: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '', word).lower()

def find_most_similar_word(word: str, dictionary: Dict[str, bool]) -> str:
    preprocessed_word = preprocess_word(word)
    
    # Check if the exact word exists in the dictionary
    if preprocessed_word in dictionary:
        return word

    # Filter dictionary words by similar length (within ±1 length difference)
    candidates = [w for w in dictionary.keys() if abs(len(w) - len(preprocessed_word)) <= 1]
    if not candidates:
        candidates = list(dictionary.keys())
    
    # Find the best match based on a weighted similarity measure
    most_similar = min(
        candidates,
        key=lambda x: (Levenshtein.distance(preprocessed_word, x), abs(len(x) - len(preprocessed_word)))
    )

    # Preserve capitalization
    if word.isupper():
        return most_similar.upper()
    elif word.istitle():
        return most_similar.capitalize()
    else:
        return most_similar

def correct_phrase(phrase: str, dictionary: Dict[str, bool]) -> str:
    words = phrase.split()
    corrected_words = [find_most_similar_word(word, dictionary) for word in words]
    return ' '.join(corrected_words)

def calculate_accuracy(corrected_phrases: List[str], ground_truth_phrases: List[str]) -> float:
    total_similarity = sum(difflib.SequenceMatcher(None, c.lower(), g.lower()).ratio() 
                           for c, g in zip(corrected_phrases, ground_truth_phrases))
    return total_similarity / len(corrected_phrases) * 100

def main():
    dictionary_path = 'tamil_dictionary.csv'
    error_phrases_path = 'error_phrases.txt'
    ground_truth_path = 'ground_truth.csv'

    start_time = time.time()

    # Load data
    dictionary = load_dictionary(dictionary_path)
    error_phrases = load_phrases(error_phrases_path)
    ground_truth_phrases = load_phrases(ground_truth_path)

    # Correct phrases
    corrected_phrases = [correct_phrase(phrase, dictionary) for phrase in error_phrases]

    # Calculate accuracy
    accuracy = calculate_accuracy(corrected_phrases, ground_truth_phrases)

    end_time = time.time()
    processing_time = end_time - start_time

    # Print results
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Processing time: {processing_time:.2f} seconds")

    # Check if accuracy meets the requirement
    if accuracy >= 90:
        print("Accuracy requirement met!")
    else:
        print("Accuracy requirement not met. Further improvements needed.")

    # Print example corrections
    print("\nExample corrections:")
    for i in range(min(5, len(error_phrases))):
        print(f"Original: {error_phrases[i]}")
        print(f"Corrected: {corrected_phrases[i]}")
        print(f"Ground truth: {ground_truth_phrases[i]}")
        print()

if __name__ == "__main__":
    main()