from rapidfuzz.distance import Levenshtein

def calculate_cer(reference, hypothesis):
    """
    Calculate the Character Error Rate (CER) between reference and hypothesis texts using RapidFuzz.
    """
    # Calculate the Levenshtein distance
    distance = Levenshtein.distance(reference, hypothesis)
    
    # Calculate CER
    cer = distance / len(reference)
    return cer

def calculate_wer(reference, hypothesis):
    """
    Calculate the Word Error Rate (WER) between reference and hypothesis texts using RapidFuzz.
    """
    # Tokenize the words
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    
    # Calculate the Levenshtein distance
    distance = Levenshtein.distance(ref_words, hyp_words)
    
    # Calculate WER
    wer = distance / len(ref_words)
    return wer

def read_file(file_path):
    """
    Read the contents of a file and return it as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def calculation(reference_file,hypothesis_file):
    # Read the contents of the files
    reference = read_file(reference_file)
    hypothesis = read_file(hypothesis_file)

    # Calculate CER and WER
    cer = calculate_cer(reference, hypothesis)
    wer = calculate_wer(reference, hypothesis)

    print(f'CER: {cer:.5f}')
    print(f'WER: {wer:.5f}')
    
    
# Example usage
reference_file = r'path to reference file'
hypothesis_file = r'path to hypothesis file'

calculation(reference_file,hypothesis_file)

