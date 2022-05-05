# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:18:36 2021

@author: kevin
"""

from flask import Flask, render_template, Response, redirect, url_for
from camera import VideoCamera
from camera1 import VideoCamera1
import cv2
import keyboard
import os
import pyttsx3

font = cv2.FONT_HERSHEY_SIMPLEX
app = Flask(__name__)
list = ['hello']
import cv2
#from model import SignPredictionModel
#from model import SignPredictionModel1
import numpy as np
import tensorflow as tf
import keyboard

# model = SignPredictionModel("ResNet50V2_No_weights_model.json", "ResNet50V2_No_weights2_model.json", "ResNet50V2_No_weights_model_weight.h5", "ResNet50V2_No_weights2_model_weight.h5")

# model = SignPredictionModel("./model7.h5", "./model10.h5")

@app.route('/')
def main():
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    #model = SignPredictionModel('./model7.h5', './model10.h5')
    return render_template('index.html', list=val())

def gen(camera):
    letters = []
    words = []
    word = ""
    while True:

        frame, roi = camera.get_frame(word)
        output = camera.get_res()

        # for i in range(len(letters)):
        #    cv2.putText(frame, letters[i], (220, 80), font, 1, (255, 255, 0), 2)
        if keyboard.is_pressed('enter'):
            if output != '0':
                if output == "nothing":
                    if words == []:
                        print(''.join(letters))
                    print(''.join(words))
                elif output == "del":
                    if len(letters) != 0:
                        letters.pop(-1)
                    else:
                        letters.pop(0)
                else:
                    letters.append(output)
            else:

                word = ''.join(letters)
                list.append(word)
                words.append(word)
                words.append(" ")
                letters.clear()
            print(output, words, letters)
            #keyboard.release('enter')


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/clear/')
def clear():
    list.pop()
    return redirect(url_for('index'))

@app.route('/val')
def val():
    list1 = list.copy()
    return list1


@app.route('/speech/')
def speech():
    list2 = ''.join(list)
    engine = pyttsx3.init()
    engine.say(list2)
    engine.runAndWait()
    return redirect(url_for('index'))


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/alpha/')
def alpha():
    return render_template('home.html', list=val())
# if flag==1:
#   model = SignPredictionModel("./model7.h5", "./model10.h5")
# else:
# model = SignPredictionModel1("./model1.h5", "./model2.h5")
def gen1(camera1):
    letters = []
    words = []
    word = ""

    while True:

        frame, roi = camera1.get_frame(word)
        output = camera1.get_res()
        # for i in range(len(letters)):
        #    cv2.putText(frame, letters[i], (220, 80), font, 1, (255, 255, 0), 2)
        if keyboard.is_pressed('enter'):
            if output != 'space':
                if output == "nothing":
                    if words == []:
                        print(''.join(letters))
                    print(''.join(words))
                elif output == "del":
                    if len(letters) != 0:
                        letters.pop(-1)
                    else:
                        letters.pop(0)
                else:
                    letters.append(output)
            else:
                word = ''.join(letters)
                list.append(word)
                words.append(word)
                words.append(" ")
                letters.clear()
            print(output, words, letters)
            keyboard.release('enter')


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/alphabet/')
def alphabet():
    return redirect(url_for('alpha'))


@app.route('/number/')
def number():
    return redirect(url_for('index'))

@app.route('/Enter/')
def Enter():
    return keyboard.press_and_release('enter')


@app.route('/video_feed1')
def video_feed1():
    return Response(gen1(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
