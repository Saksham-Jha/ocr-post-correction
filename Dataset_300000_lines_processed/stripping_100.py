import os

def split_file_into_chunks(input_file, output_dir, chunk_size=100):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    num_chunks = (len(lines) + chunk_size - 1) // chunk_size  # Calculate number of chunks needed
    
    for chunk_num in range(num_chunks):
        start = chunk_num * chunk_size
        end = min(start + chunk_size, len(lines))
        chunk = lines[start:end]
        
        output_file = os.path.join(output_dir, f"{chunk_num + 1}.txt")
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.writelines(chunk)

    print(f"Successfully split {input_file} into {num_chunks} files in {output_dir}.")

# Example usage:
input_file = "path to input file"
output_directory = "path to output directory"

split_file_into_chunks(input_file, output_directory)
