# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:10:22 2021

@author: kevin
"""
import cv2
from model import SignPredictionModel1
import numpy as np
import tensorflow as tf
import keyboard

# model = SignPredictionModel("ResNet50V2_No_weights_model.json", "ResNet50V2_No_weights2_model.json", "ResNet50V2_No_weights_model_weight.h5", "ResNet50V2_No_weights2_model_weight.h5")

model = SignPredictionModel1("./model1.h5", "./model2.h5")

font = cv2.FONT_HERSHEY_SIMPLEX


class VideoCamera1(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self, word):
        _, fr = self.video.read()

        crop_fr = fr[100:300, 100:300]
        crop_fr = tf.keras.applications.resnet_v2.preprocess_input(crop_fr)
        # roi = cv2.resize(crop_fr, (200, 200))
        roi = crop_fr
        self.pred, self.conf = model.predict_sign(roi[np.newaxis, :, :])

        cv2.rectangle(fr, (100, 100), (300, 300), (255, 0, 0), 2)
        cv2.putText(fr, self.pred, (100, 80), font, 1, (0, 0, 255), 2)
        cv2.putText(fr, word, (220, 80), font, 1, (255, 255, 0), 2)
        # cv2.putText(fr, self.conf, (160, 80), font, 1, (255, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes(), roi

    def get_res(self):
        return self.pred