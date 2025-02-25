"""Module with functions for training the post-correction sequence-to-sequence model.

Early stopping on the validation set CER is used for determining the best model.

Copyright (c) 2021, Shruti Rijhwani
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
"""


import dynet as dy
import logging
import random
from utils import DataReader, ErrorMetrics
import time
from constants import EPOCHS, PATIENCE

# Changes made for configuring logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create console handler and set level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create file handler and set level to info
file_handler = logging.FileHandler('training.log')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Add formatter to handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class Seq2SeqTrainer:
    def __init__(self, model, output_name=None):
        self.model = model
        self.datareader = DataReader()
        self.metrics = ErrorMetrics()
        self.output_name = output_name

    def train(
        self,
        train_data,
        val_data,
        epochs=EPOCHS,
        patience=PATIENCE,
        pretrain=False,
        minibatch_size=1,
    ):
        trainer = dy.SimpleSGDTrainer(self.model.model)

        logging.info("Training data length: %d" % len(train_data))
        logging.info("Validation data length: %d" % len(val_data))

        for e in range(epochs):
            start_time = time.time()
            logging.info("Epoch: %d" % e)
            epoch_loss = 0.0
            random.shuffle(train_data)

            for i in range(0, len(train_data), minibatch_size):
                cur_size = min(minibatch_size, len(train_data) - i)
                losses = []
                dy.renew_cg()
                for (src1, src2, tgt) in train_data[i : i + cur_size]:
                    losses.append(self.model.get_loss(src1, src2, tgt))
                batch_loss = dy.esum(losses)
                batch_loss.backward()
                trainer.update()
                epoch_loss += batch_loss.scalar_value()
            logging.info("Epoch loss: %0.4f" % (epoch_loss / len(train_data)))

            if not pretrain:
                cur_cer, cur_wer = self.metrics.get_average_cer(
                    self.model, val_data, output_file=None, write_pgens=False
                )
                if cur_cer < self.model.best_val_cer:
                    self.model.save()
                    self.model.best_val_cer = cur_cer
                    best_val_epoch = e
                    logging.info("Model saved at epoch: {}".format(best_val_epoch))
                logging.info("VAL CER: %0.4f" % (cur_cer))
                logging.info("VAL WER: %0.4f" % (cur_wer))
                if cur_cer == 0:
                    logging.info("Validation CER is zero. End training.")
                    break

            logging.info("--- %s seconds ---" % (time.time() - start_time))
            logging.info("\n")

            if not pretrain:
                if e - best_val_epoch > patience:
                    logging.info("Patience reached. End training.")
                    break

    def train_model(
        self, train_src1, train_src2, train_tgt, val_src1, val_src2, val_tgt
    ):
        train_data = self.datareader.read_parallel_data(
            self.model, train_src1, train_src2, train_tgt
        )
        val_data = self.datareader.read_parallel_data(
            self.model, val_src1, val_src2, val_tgt
        )
        self.train(train_data, val_data)