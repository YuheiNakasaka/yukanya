import numpy as np
import cv2
import os
import sys
import re
from keras.models import Sequential, model_from_json
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPool2D
from keras.layers.core import Dense,Activation,Dropout,Flatten
from keras.utils import np_utils
from keras.layers.core import Dense
from keras.optimizers import RMSprop
from keras.preprocessing.image import load_img
from keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import matplotlib.pyplot as plt

def member_to_name(member):
    if member == "akariuemura":
        return "植村あかり"
    elif member == "karinmiyamoto":
        return "宮本佳林"
    elif member == "manakainaba":
        return "稲場愛香"
    elif member == "rurudanbara":
        return "段原瑠々"
    elif member == "sayukitakagi":
        return "高木紗友希"
    elif member == "tomokokanazawa":
        return "金澤朋子"
    elif member == "yukamiyazaki":
        return "宮崎由加"

def main():
    if not (len(sys.argv) == 2 and re.match('.+\.(jpg|jpeg|png)', sys.argv[1])):
        print('Error: set image path.')
        return False

    img_path = sys.argv[1]
    model_path = "YukanyaModel_google_ameba.json"
    weight_path = "YukanyaModel_google_ameba.h5"
    label = [
      "akariuemura",
      "karinmiyamoto",
      "manakainaba",
      "rurudanbara",
      "sayukitakagi",
      "tomokokanazawa",
      "yukamiyazaki"
    ]

    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    faces = face_cascade.detectMultiScale(img)
    face_data = []
    for (x,y,w,h) in faces:
        print('Face ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h))
        face = img[y:y+h, x:x+w]
        face = cv2.resize(face, (64, 64))
        face_data.append(face)
    face_img = face_data[0]

    # cv2.imshow('main', face_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    imgarray = []
    imgarray.append(img_to_array(face_img))
    imgarray = np.array(imgarray)
    imgarray.astype('float32')
    model = model_from_json(open(model_path,'r').read())
    model.load_weights(weight_path)
    model.compile(loss='categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])

    y_pred = model.predict(imgarray)
    sorted_results = []
    for i, score in enumerate(y_pred[0]):
        sorted_results.append([score *  100, member_to_name(label[i])])
    sorted_results.sort()
    for result in sorted_results[::-1]:
        print(result[1] + ': ' + str(result[0]) + '%')

if __name__ == '__main__':
    main()