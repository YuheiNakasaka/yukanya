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

def main():
    #画像パス
    if not (len(sys.argv) == 2 and re.match('.+\.(jpg|jpeg|png)', sys.argv[1])):
        print('Error: set image path.')
        return False

    img_path = sys.argv[1]
    #モデルパス
    model_path = "YukanyaModel.json"
    #重みパス
    weight_path = "YukanyaModel.h5"
    #ラベル
    label = members = [
      "akariuemura",
      "karinmiyamoto",
      "manakainaba",
      "rurudanbara",
      "sayukitakagi",
      "tomokokanazawa",
      "yukamiyazaki"
    ]
    # 顔認識
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    faces = face_cascade.detectMultiScale(img)
    face_data = []
    for (x,y,w,h) in faces:
        face = img[y:y+h, x:x+w]
        face = cv2.resize(face, (64, 64))
        img = Image.fromarray(face)
        face_data.append(img)
    face_img = face_data[0]

    # #検出した顔データの確認
    # plt.imshow(face_img)
    # plt.show()

    imgarray = []
    imgarray.append(img_to_array(face_img))
    imgarray = np.array(imgarray)
    imgarray.astype('float32')

    #モデルの読み込み
    model = model_from_json(open(model_path,'r').read())
    #重みの読み込み
    model.load_weights(weight_path)
    #コンパイル
    model.compile(loss='categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])
    #テスト画像を入力し、結果を出力する
    y_pred = model.predict(imgarray)
    print(y_pred)
    #出力結果をクラスラベルから整数値に変換
    y_pred = np.argmax(y_pred, axis=1)
    print(y_pred)
    print("予測結果:",label[int(y_pred)])

if __name__ == '__main__':
    main()