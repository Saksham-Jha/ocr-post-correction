import os

# Function to process the provided file and store OCR aligned and GS aligned sections separately
def extract_aligned_sections(input_file):
    ocr_aligned_text = ""
    gs_aligned_text = ""

    in_ocr_aligned = False
    in_gs_aligned = False

    with open(input_file, 'r', encoding='utf-8') as file:
        current_section = ""
        while True:
            char = file.read(1)
            if not char:
                break  

            current_section += char

            if current_section.endswith('[OCR_aligned]'):
                in_ocr_aligned = True
                in_gs_aligned = False
                current_section = ""
                continue
            elif current_section.endswith('[ GS_aligned]'):
                in_ocr_aligned = False
                in_gs_aligned = True
                current_section = ""
                continue

            if in_ocr_aligned:
                ocr_aligned_text += char
            elif in_gs_aligned:
                gs_aligned_text += char
    
    ocr_aligned_text = ocr_aligned_text[1:-13]
    gs_aligned_text = gs_aligned_text[1:-1]
    print(len(ocr_aligned_text))
    print(len(gs_aligned_text))
    return ocr_aligned_text, gs_aligned_text

# Function to create directories if they don't exist
def create_directories(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Function to process aligned sections, strip lines ending with '.', and write to output files
def process_aligned_sections(ocr_aligned, gs_aligned, output_directory, filename):
    ocr_lines = []
    gs_lines = []

    ocr_line = ""
    gs_line = ""

    for ocr_char, gs_char in zip(ocr_aligned, gs_aligned):
        ocr_line += ocr_char
        gs_line += gs_char

        # Check for complete lines based on period ('.')
        if ocr_char == '.' and gs_char == '.':
            ocr_lines.append(ocr_line)
            gs_lines.append(gs_line)
            # print(len(ocr_lines))
            # print(len(gs_lines))
            ocr_line = ""
            gs_line = ""

    # Add any remaining text in ocr_line and gs_line to their respective lists
    if ocr_line:
        ocr_lines.append(ocr_line)
    if gs_line:
        gs_lines.append(gs_line)

    # Write to output files
    ocr_output_path = os.path.join(output_directory, 'ocr_input', filename)
    gs_output_path = os.path.join(output_directory, 'corrected_target', filename)

    with open(ocr_output_path, 'w', encoding='utf-8') as ocr_file:
        ocr_file.write('\n'.join(ocr_lines))

    with open(gs_output_path, 'w', encoding='utf-8') as gs_file:
        gs_file.write('\n'.join(gs_lines))

    print(f"Files written to: {ocr_output_path}, {gs_output_path}")

# Main function to process 100 text files sequentially
def process_all_files(input_directory, output_directory):
    for i in range(0, 150):
        input_file_path = os.path.join(input_directory, f"{i}.txt")
        print(f"Processing file: {input_file_path}")

        # Extract aligned sections from the input file
        ocr_aligned, gs_aligned = extract_aligned_sections(input_file_path)

        # Create directories if they don't exist
        create_directories([
            os.path.join(output_directory, 'ocr_input'),
            os.path.join(output_directory, 'corrected_target')
        ])

        # Process aligned sections and write to output files
        filename = f"{i}.txt"
        process_aligned_sections(ocr_aligned, gs_aligned, output_directory, filename)

    print("Processing completed.")

# Example usage:
input_directory = r'Eng - icdar 2019' # path to Eng - icdar 2019
output_directory = r'output_files_new' # path to output_files folder

process_all_files(input_directory, output_directory)
