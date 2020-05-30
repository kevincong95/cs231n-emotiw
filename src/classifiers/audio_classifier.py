# -*- coding: utf-8 -*-
"""audio-final-classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wHOFUEoOQsLsixPYWLnuwZweSSP9xkVN
"""

import glob
import os

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import Normalizer

from .utils import unzip_folder


class AudioClassifier:
    """
    Classifies sentiment based on audio extracted from videos
    """

    def __init__(self, audio_folder , model_location=None, is_test=True, batch_size=32):
        """
        @param audio_folder   The folder where the arrays of processed audio embeddings are stored. If
                              ends with .zip, this should be a single zip
                              file containing the embeddings. Paths can either be accessed by a local
                              folder or a GDrive mounted path.
        @param model_location The pre-trained model to perform predictions
        @param is_test        If set to True, we assume that we are testing . If false, the evaluate
                              function will return a score.
        @param batch_size     The batch size used to feed into the model evaluation
        """
        self.audio_folder = audio_folder
        self.is_test = is_test
        self.model_location = model_location
        self.batch_size = batch_size
        print(f"AudioClassifier created with audio_folder = {audio_folder} , is_test = {is_test} , model_location = {model_location}")

    def predict(self, layer=None):
        """
        Performs sentiment classification prediction on preprocessed audio files
        @param layer: If None, performs normal sentiment classification.
                      If not None, returns the values from the intermediate layers.
        return:
            - The model prediction result
            - The video file names for each of the rows returned in model.predict
              (without the .mp4 suffix)
        """
        folder = unzip_folder(self.audio_folder, "audio_tmp")
        X = np.load(os.path.join(folder, 'audio-pickle-all-X-openl3.pkl'), allow_pickle=True)

        if "https://" in self.model_location or "http://" in self.model_location:
            downloaded_model_path = tf.keras.utils.get_file("audio-classifier", self.model_location)
            model = tf.keras.models.load_model(downloaded_model_path)
        else:
            model = tf.keras.models.load_model(self.model_location)

        if layer is not None:
            print(f"Customizing model by returning layer {layer}")
            model = tf.keras.models.Model(model.input, model.get_layer(layer).output)

        normalizer = Normalizer()
        for i in range(0, X.shape[0]):
            X[i] = normalizer.fit_transform(X[i])

        # The original pre-processing created the X array using the sorted order of the video files
        audio_pickles = sorted(next(os.walk(os.path.join("train-tiny-audio", "audio-pickle")))[2])
        samples = map(lambda x: x.split(".mp4")[0], audio_pickles)

        return model.predict(X, batch_size=self.batch_size), samples

    def summary(self):
        """
        Summarizes the pre-trained model
        """
        model = tf.keras.models.load_model(self.model_location)
        model.summary()

    def evaluate(self):
        """
        Evaluates the audio_folder files on the pre-trained model
        return: The evaluation results
        """
        if self.is_test:
            print("Evaluation cannot be done in test-mode")
            return

        folder = unzip_folder(self.audio_folder, "audio_tmp")
        X = np.load(os.path.join(folder, 'audio-pickle-all-X-openl3.pkl'), allow_pickle=True)
        Y = np.load(os.path.join(folder, 'audio-pickle-all-Y-openl3.pkl'), allow_pickle=True)
        model = tf.keras.models.load_model(self.model_location)
        normalizer = Normalizer()
        for i in range(0,X.shape[0]):
            X[i] = normalizer.fit_transform(X[i])

        return model.evaluate(X , Y)
