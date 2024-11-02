import random
import re
import csv

def create_phonetic_errors(word):
    # Common Thanglish phonetic variations
    phonetic_rules = {
        'th': 't',
        't': 'th',
        'dh': 'd',
        'd': 'dh',
        'z': 's',
        'sh': 's',
        'ch': 'c',
        'kk': 'k',
        'pp': 'p',
        'nn': 'n',
        'aa': 'a',
        'ee': 'e',
        'oo': 'o',
        'u': 'oo',
        'i': 'ee',
        'gh': 'g',
        'ng': 'n',
        'ai': 'ay',
        'ei': 'ey'
    }
    
    # Randomly select and apply a phonetic error if possible
    for pattern, replacement in phonetic_rules.items():
        if pattern in word.lower() and random.random() < 0.3:  # 30% chance of error
            return word.replace(pattern, replacement)
            
    return word

def create_spelling_errors(word):
    if len(word) < 3:
        return word
        
    error_types = [
        # Swap adjacent characters
        lambda w: w[:random.randint(0, len(w)-2)] + w[random.randint(0, len(w)-2)+1] + w[random.randint(0, len(w)-2)] + w[random.randint(0, len(w)-2)+2:] if len(w) > 3 else w,
        # Double a letter
        lambda w: w[:random.randint(0, len(w)-1)] + w[random.randint(0, len(w)-1)] + w[random.randint(0, len(w)-1):],
        # Remove a letter
        lambda w: w[:random.randint(0, len(w)-1)] + w[random.randint(0, len(w)-1)+1:] if len(w) > 3 else w,
        # Add a common typing error
        lambda w: w.replace('a', 'q').replace('s', 'a').replace('n', 'm') if random.random() < 0.3 else w
    ]
    
    if random.random() < 0.3:  # 30% chance of spelling error
        error_func = random.choice(error_types)
        return error_func(word)
    return word

def process_sentence(sentence):
    # Split sentence into words
    words = sentence.strip().split()
    
    # Ensure at least 3 words are modified
    num_words_to_modify = min(2, len(words))
    if num_words_to_modify > 0:
        num_words_to_modify = random.randint(1, num_words_to_modify)
    words_to_modify = random.sample(range(len(words)), num_words_to_modify)
    
    # Apply errors to selected words
    for idx in words_to_modify:
        if random.random() < 0.5:
            words[idx] = create_phonetic_errors(words[idx])
        else:
            words[idx] = create_spelling_errors(words[idx])
    
    return ' '.join(words)

def process_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            sentences = [row[0] for row in reader if row]  # Read the first column of each row
        
        modified_sentences = []
        for sentence in sentences:
            if sentence.strip():  # Skip empty lines
                modified = process_sentence(sentence)
                modified_sentences.append(modified)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for sentence in modified_sentences:
                f.write(sentence + '\n')
                
        print(f"Successfully processed {len(modified_sentences)} sentences")
        
        # Print a few examples of the modifications
        print("\nExample modifications:")
        for i in range(min(8, len(sentences))):
            print(f"\nOriginal: {sentences[i].strip()}")
            print(f"Modified: {modified_sentences[i].strip()}")
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_file = "phrases_cleaned.csv"  # Your input CSV file with the phrases
    output_file = "error_phrases.txt"  # Output file with modified phrases
    
    # Process the file
    process_file(input_file, output_file)