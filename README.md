# Tamil Phonetic Error Correction

A Python tool for correcting Tamil phrases typed phonetically in English, using a dictionary-based approach combined with similarity metrics to correct spelling and phonetic errors.

## Features

* Corrects Tamil phrases typed in English with phonetic spelling errors
* Uses a Levenshtein distance-based algorithm to match similar words from a provided dictionary
* Achieves high accuracy by comparing each corrected phrase against a ground truth file
* Reports accuracy and processing time metrics to evaluate performance

## Requirements

* Python 3.6 or higher
* Required Python packages: Levenshtein, difflib, csv

Install dependencies with:

```bash
pip install python-Levenshtein
```

## Usage

### Input Files

1. **Dictionary**: A CSV file with one valid Tamil word (typed in English) per line
2. **Error Phrases**: A TXT file with one incorrect Tamil phrase (typed in English) per line
3. **Ground Truth**: A CSV file with one corrected phrase per line for accuracy evaluation

### Running the Script

Place the input files in the same directory as the script and run:

```bash
python main.py
```

### Output

* **Accuracy**: Percentage of correctly corrected phrases
* **Processing Time**: Total time taken to process all phrases

Sample output:
```
Accuracy: 90.31%
Processing time: 0.20 seconds
Accuracy requirement met!
```

## Example Corrections

The script will print a few example corrections as follows:

```
Errored: naan kadaikkoo vengayam vangaren
Corrected: naan kadaikku vengayam vaangaren
Ground truth: Naan kadaikku vengayam vaangaren
```

## How It Works

1. **Exact Match Check**: Words already in the dictionary remain unchanged
2. **Length-Based Candidate Filtering**: Filters candidates to words with similar length to improve matching accuracy
3. **Weighted Similarity Matching**: Uses Levenshtein distance with length as a secondary criterion

## Future Improvements

* Optimize for larger datasets to further reduce processing time
* Integrate additional phonetic similarity measures
