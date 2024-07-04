import os

def split_paragraphs(input_directory):
    # Check if the input directory exists
    if not os.path.exists(input_directory):
        print(f"Directory does not exist: {input_directory}")
        return

    # Process each .txt file in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_directory, filename)
            print(f"Processing file: {input_file_path}")

            # Read the content of the file
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Split the content into separate lines at each '.'
            lines = content.split('.')
            stripped_lines = [line.strip() for line in lines if line.strip()]

            # Write the new content back to the same file
            with open(input_file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(stripped_lines))

            print(f"File processed and written: {input_file_path}")

    print("Processing completed.")

# Example usage:
input_directory = r'path to input directory' 
split_paragraphs(input_directory)
