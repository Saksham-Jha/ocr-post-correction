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
### Testing

For testing with a single-source model, modify the experimental settings in `test_single-source.sh`.

Then run
```
bash test_single-source.sh
```

For multisource, use `test_multi-source.sh`.

### Evaluation

Evaluation can be performed using `evaluate_cer_wer.py`, which calculates the Character Error Rate (CER) and Word Error Rate (WER) between reference and hypothesis files.

### Experiments

| Dataset Used                                  | Metrics Before and During Training (Validation Set)         | Metrics on the Test Set                                                  | Remarks                                                                                                                                                         |
|-----------------------------------------------|------------------------------------------------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| English ICDAR 2019 (complete with first 11 files for pretraining and remaining for training and testing) | CER: 0.12508<br>WER: 0.30903<br>Pretraining completed         | -                                                                       | Pretraining was successfully completed. However, the training encountered a memory error. Similar error also occurred on Google Colab (`Training on Google Colab.ipynb`). I tried adjusting the learning rate, batch size but the memory issue still persisted.           |
| English ICDAR 2019 (Smaller dataset with first 6 files for pretraining and next 40 for training and testing) | CER: 0.04718<br>WER: 0.15113<br>Pretraining completed         | -                                                                       | Pretraining was successfully completed. However, the training encountered a memory error. Similar error also occurred on Google Colab (`Training on Google Colab.ipynb`).           |
| MiBio Book Dataset (complete with first 10 files for pretraining and remaining for training and testing) | CER: 0.0206<br>WER: 0.0917<br>During training (25 epochs):<br>VAL CER: 0.0129 (Epoch 0) -> 0.0068 (Epoch 25)<br>VAL WER: 0.0338 (Epoch 0) -> 0.0183 (Epoch 25) | Before Testing:<br>CER: 0.02026<br>WER: 0.0903<br>After Testing:<br>CER: 0.0069<br>WER: 0.01906<br>Improvement:<br>CER: 65.94%<br>WER: 78.89% | Though the results on the test set are good, overfitting might have occurred as the results on other testing were not as good.                                   |
| Dataset 300000 lines (smaller dataset with 1 file for pretraining and 29 files for training and testing, each file having 100 lines of text) | CER: 0.05772<br>WER: 0.28150<br>Pretraining completed. During training, VAL CER and VAL WER degraded continuously from epoch 0 to epoch 3, so training was stopped. | -                                                                       | The reason for the degradation is unclear, but training on this dataset should be beneficial as it includes manually infused errors such as character substitution, missing characters, adding false characters, and removing punctuation. |

**Conclusion**

The experiments revealed key challenges. Addressing these with memory optimization, regularization techniques, and refined data augmentation strategies can enhance model performance and generalizability. Future efforts should focus on these areas to achieve more robust results.


For additional details, refer to `README_original.md` and `firstpass.md`.