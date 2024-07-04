#!/bin/bash

# --------------------- REQUIRED: Modify for each dataset and/or experiment ---------------------

# Set training and development set files
train_src="sample_dataset7/postcorrection/training/train_src1.txt"
train_tgt="sample_dataset7/postcorrection/training/train_tgt.txt"

dev_src="sample_dataset7/postcorrection/training/dev_src1.txt"
dev_tgt="sample_dataset7/postcorrection/training/dev_tgt.txt"

# Set experiment parameters
expt_folder="my_expt_singlesource/"

dynet_mem=3000 # Memory in MB available for training

params="--pretrain_dec --pretrain_s2s --pretrain_enc --pointer_gen --coverage --diag_loss 2"
pretrained_model_name="my_pretrained_model"
trained_model_name="my_trained_model"

# ------------------------------END: Required experimental settings------------------------------

# Create experiment directories if not already created
mkdir -p $expt_folder/debug_outputs
mkdir -p $expt_folder/models
mkdir -p $expt_folder/outputs
mkdir -p $expt_folder/train_logs
mkdir -p $expt_folder/vocab

# Load the pretrained model and train the model using manually annotated training data (add --dynet-gpu for using GPU)
# See postcorrection/opts.py for all the options
python postcorrection/multisource_wrapper.py \
--dynet-mem $dynet_mem \
--dynet-autobatch 0 \
--train_src1 $train_src \
--train_tgt $train_tgt \
--dev_src1 $dev_src \
--dev_tgt $dev_tgt \
$params \
--single \
--vocab_folder $expt_folder/vocab \
--output_folder $expt_folder \
--load_model $expt_folder"/pretrain_models/"$pretrained_model_name \
--model_name $trained_model_name \
--train_only
