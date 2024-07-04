from transformers import AutoTokenizer
import random
import re
import os
from tqdm import tqdm
from string import ascii_letters

def tokenizer_check_if_text_too_long(text, tokenizer, max_length):
    data = tokenizer.batch_encode_plus([text], max_length=max_length, truncation=True, return_overflowing_tokens=True)
    if len(data["input_ids"]) > 1:
        return True
    else:
        return False

def delete_characters(text, char_delete_percentage=0.01):
    modified_line = []
    for char in text:
        if random.random() > char_delete_percentage or char.isdigit():
            modified_line.append(char)
    return "".join(modified_line)

def insert_characters(text, augmentation_probability=0.01):
    modified_line = []
    for char in text:
        if random.random() <= augmentation_probability and char.isalpha():
            modified_line.append(random.choice(ascii_letters))
        modified_line.append(char)
    return "".join(modified_line)

def replace_characters(text, augmentation_probability=0.01):
    modified_line = []
    for char in text:
        if random.random() <= augmentation_probability and char.isalpha():
            if char.lower() == 'o' and random.random() < 0.5:
                # Replace 'o' with '0' or vice versa with 50% probability
                modified_line.append(random.choice(['o', 'O', '0', 'O', 'o']))
            elif char.lower() == 'l' and random.random() < 0.5:
                # Replace 'l' with '1' or vice versa with 50% probability
                modified_line.append(random.choice(['l', '1', 'L', 'l', '1']))
            elif char.upper() == 'I' and random.random() < 0.5:
                # Replace 'I' with '1' or vice versa with 50% probability
                modified_line.append(random.choice(['I', '1', 'i', 'I', '1']))
            elif char.upper() == 'S' and random.random() < 0.5:
                # Replace 'S' with '$' or vice versa with 50% probability
                modified_line.append(random.choice(['S', '$', 's', 'S', '$']))
            elif char.upper() == 'B' and random.random() < 0.5:
                # Replace 'B' with '8' or vice versa with 50% probability
                modified_line.append(random.choice(['B','8','b','8','B']))
            else:
                modified_line.append(random.choice(ascii_letters))
        else:
            modified_line.append(char)
    return "".join(modified_line)

def swap_characters_case(text, augmentation_probability=0.005):
    modified_line = []
    for char in text:
        if random.random() <= augmentation_probability:
            char = char.swapcase()
        modified_line.append(char)
    return "".join(modified_line)

def lower_case_words(text, augmentation_probability=0.5):
    modified_line = []
    for word in text.split():
        if not word[0].islower() and random.random() <= augmentation_probability:
            word = word.lower()
        modified_line.append(word)
    return " ".join(modified_line)

clean_chars = re.compile(r'[^A-Za-z0-9,.!?’\'$%€()\-\s]', re.MULTILINE)
def cleanup(text):
    text = clean_chars.sub('', text)
    return text

clean_punctuation = re.compile(r"(?<!\d)[.,;:'?!](?!\d)")
def remove_punctuation(text):
    return clean_punctuation.sub("", text)

def combine_sentences(text, sentences, augmentation_probability=1):
    if random.random() < augmentation_probability:
        sentences_to_sample = random.randint(0, 10)
        augmentation_sentences = random.sample(sentences, sentences_to_sample)
        return text + " " + " ".join(augmentation_sentences)
    else:
        return text

def delete_word(text, augmentation_probability=0.001):
    if random.random() < augmentation_probability:
        words = text.split()
        if len(words) < 3:
            return text
        word_to_remove = random.randint(0, len(words) - 1)
        words.pop(word_to_remove)
        return " ".join(words)
    else:
        return text

if __name__ == "__main__":
    data_file = r"C:\Users\Saksham Jha\Desktop\Spelling correction\spelling\data\data.txt"
    num_lines = 300000

    sentences = []
    with open(data_file, 'r', encoding='utf-8') as file:
        for _ in tqdm(range(num_lines)):
            line = file.readline().strip()
            line = cleanup(line)
            sentences.append(line)

    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")

    with open("corrected_text_300000.txt", "w", encoding='utf-8') as correct_output, \
         open("incorrect_text_300000.txt", "w", encoding='utf-8') as incorrect_output:

        for line in tqdm(sentences, total=len(sentences)):
            if len(line) < 1:
                continue

            original_line = line

            if tokenizer_check_if_text_too_long(line, tokenizer, max_length=1024):
                print(f"Skipping line as it's too long ({len(line)}):\n" + line)
                continue

            new_line_corrected = original_line  # Use original_line as corrected version

            if random.random() > 0.02:
                new_line = delete_word(line)
                new_line = delete_characters(new_line)
                new_line = insert_characters(new_line)
                new_line = replace_characters(new_line)
                new_line = swap_characters_case(new_line)
                new_line = lower_case_words(new_line)
                new_line = remove_punctuation(new_line)
            else:
                new_line = line

            correct_output.write(f'{new_line_corrected.strip()}\n')
            incorrect_output.write(f'{new_line.strip()}\n')

    print("Files 'corrected_text.txt' and 'incorrect_text.txt' have been created.")
