### Setting Up Environment and Dependencies

To run the code, ensure Python 3.7.0 is installed. It is recommended to create a virtual environment. Use the following command to install the necessary packages inside the virtual environment:

```bash
pip install -r postcorr_requirements.txt
```

### Preprocessing

1. **Data Preparation**

   - **English ICDAR 2019:**
     Begin preprocessing with the `Eng-icdar2019` folder containing text files. Use the `Dataset_Eng_icdar 2019 processed/process.py` script on these files. The processed files will be found in `Dataset_Eng_icdar 2019 processed/corrected_target` and `Dataset_Eng_icdar 2019 processed/ocr_input`.

   - **MiBio Book Dataset:**
     This is a preprocessed dataset available on [GitHub](https://github.com/jie-mei/MiBio-OCR-dataset/tree/master). The files are located in `Dataset_book_MiBio`.

   - **Dataset 300000 lines:**
     This dataset consists of 300000 lines of English text (news, wiki, etc.). The raw file is `Dataset_300000_lines_processed/data.txt`. Run the `Dataset_300000_lines_processed/generate_new.py` script (it uses some additional libraries that can be installed using `Dataset_300000_lines_processed/requirements.txt`) to generate corrected and incorrected files, which are currently located in `Dataset_300000_lines_processed/corrected_target` and `Dataset_300000_lines_processed/ocr_input`, respectively. For training, you can split these files into several smaller files using `Dataset_300000_lines_processed/stripping_100.py`.

2. **Dataset Construction**
   
   - Use some incorrect files from the processed files (any dataset) and place them in `sample_dataset_new/text_outputs/uncorrected/src1` for pretraining.
   - Move the remaining corresponding files from the processed files to:
     - `sample_dataset_new/text_outputs/corrected/src1` (for corrected data)
     - `sample_dataset_new/text_outputs/corrected/tgt` (target data)
   - For sample dataset , look at `sample_dataset_English_ICDAR`, `sample_dataset_book(MiBio dataset)` and  `sample_dataset`.
   
   As recommended in `firstpass.md`, specifically in the "Constructing a Post-Correction Dataset" section:

   - **Corrected Section:**
     Ensure that each text file contains one sentence or paragraph per line.

   - **Uncorrected Section:**
     Split the text at the sentence level so that each line represents one sentence.

3. **Final Dataset Preparation**
   
   Run `utils/run_prep_data.py` to finalize preprocessing and generate the dataset.

### Pretraining and Training

For a single-source model, modify the experimental settings in `train_single-source.sh` and `train_model.sh` to point to the appropriate dataset and desired output folder.

1. **Pretraining**
   
   Execute `train_single-source.sh` initially for pretraining.

2. **Training**
   
   After pretraining, use the following command for training:

   ```bash
   bash train_model.sh
   ```

### Evaluation

Evaluation can be performed using `evaluate_cer_wer.py`, which calculates the Character Error Rate (CER) and Word Error Rate (WER) between reference and hypothesis files.

For additional details, refer to `README_original.md` and `firstpass.md`.