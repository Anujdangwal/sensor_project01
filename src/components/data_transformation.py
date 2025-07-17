from tensorflow.keras.preprocessing.image import ImageDataGenerator
from src.logger import logging
from src.exception import CustomException
import os
import sys

class ImageDataPipeline:
    def __init__(self, image_dir, target_size=(256, 256), batch_size=32):
        self.image_dir = image_dir
        self.target_size = target_size
        self.batch_size = batch_size

        self.train_datagen = ImageDataGenerator(
            rescale=1.0 / 255,
            validation_split=0.2,
            rotation_range=15,
            zoom_range=0.1,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            horizontal_flip=True,
        )

    def get_generators(self):
        try:
            logging.info("Preparing training and validation generators...")

            train_generator = self.train_datagen.flow_from_directory(
                self.image_dir,
                target_size=self.target_size,
                batch_size=self.batch_size,
                class_mode='categorical',
                subset='training',
                shuffle=True,
                seed=42
            )

            val_generator = self.train_datagen.flow_from_directory(
                self.image_dir,
                target_size=self.target_size,
                batch_size=self.batch_size,
                class_mode='categorical',
                subset='validation',
                shuffle=False,
                seed=42
            )

            return train_generator, val_generator

        except Exception as e:
            logging.error("Error while creating image data generators", exc_info=True)
            raise CustomException(e, sys)