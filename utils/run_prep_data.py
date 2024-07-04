import subprocess

# Define the absolute paths
output_folder = "C:\\Users\\Saksham Jha\\Desktop\\ocr\\ocr-post-correction\\sample_dataset7\\postcorrection"
unannotated_src1 = "C:\\Users\\Saksham Jha\\Desktop\\ocr\\ocr-post-correction\\sample_dataset7\\text_outputs\\uncorrected\\src1"
annotated_src1 = "C:\\Users\\Saksham Jha\\Desktop\\ocr\\ocr-post-correction\\sample_dataset7\\text_outputs\\corrected\\src1"
annotated_tgt = "C:\\Users\\Saksham Jha\\Desktop\\ocr\\ocr-post-correction\\sample_dataset7\\text_outputs\\corrected\\tgt"

# Define the command to run the script
command = [
    "python", "prepare_data.py",
    "--unannotated_src1", unannotated_src1,
    "--annotated_src1", annotated_src1,
    "--annotated_tgt", annotated_tgt,
    "--output_folder", output_folder,
]

# Run the command
result = subprocess.run(command, capture_output=True, text=True)

# Print the output and errors (if any)
print("Output:\n", result.stdout)
print("Errors:\n", result.stderr)
