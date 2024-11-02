import re
import csv

def extract_tanglish_words(filename):
    # Dictionary to store word pairs
    word_pairs = []
    current_category = ""
    
    # Read the text file
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Check if line is a category header
            if line.startswith('**') and line.endswith('**') and not re.match(r'\d+\.', line):
                current_category = line.strip('**').strip()
                continue
            
            # Match numbered entries with Tanglish-English pairs
            match = re.match(r'\d+\.\s*\*\*([\w\s]+)\*\*\s*-\s*(.+)$', line)
            if match:
                tanglish = match.group(1).strip()
                english = match.group(2).strip()
                
                word_pairs.append({
                    'category': current_category,
                    'tanglish': tanglish,
                    'english': english,
                    'number': int(line.split('.')[0])
                })
    
    return word_pairs

def save_to_csv(word_pairs, output_filename='tanglish_vocabulary.csv'):
    # Write to CSV file
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['number', 'category', 'tanglish', 'english']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for pair in sorted(word_pairs, key=lambda x: x['number']):
            writer.writerow(pair)

def main():
    input_filename = 'Thanglish.txt'  # Your input text file name
    output_filename = 'tanglish_vocabulary.csv'
    
    try:
        # Extract Tanglish-English word pairs
        word_pairs = extract_tanglish_words(input_filename)
        
        # Save to CSV
        save_to_csv(word_pairs, output_filename)
        
        # Print summary
        print(f"Successfully extracted {len(word_pairs)} Tanglish-English word pairs")
        print("\nSample entries:")
        for pair in word_pairs[:5]:
            print(f"{pair['number']}. {pair['category']}: {pair['tanglish']} - {pair['english']}")
            
        # Print categories summary
        categories = set(pair['category'] for pair in word_pairs)
        print(f"\nFound {len(categories)} categories:")
        for category in sorted(categories):
            category_count = len([p for p in word_pairs if p['category'] == category])
            print(f"- {category}: {category_count} words")
            
    except FileNotFoundError:
        print(f"Error: Could not find the input file '{input_filename}'")
        print("Please make sure the file exists in the same directory as this script.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()