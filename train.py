import cv2
import numpy as np
import os
import re
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical
from keras.layers import Activation, Conv2D, Dense, Flatten, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split

members = [
  "akariuemura",
  "karinmiyamoto",
  "manakainaba",
  "rurudanbara",
  "sayukitakagi",
  "tomokokanazawa",
  "yukamiyazaki"
]
member_base_dir = "members"
test_base_dir = "test"

# 訓練
X_train = []
y_train = []
for i, member in enumerate(members):
    member_dir = member_base_dir + '/' + member + '/'
    for filename in os.listdir(member_dir):
        if not re.match('.+.jpg', filename): continue
        filepath = member_dir + filename
        img = img_to_array(load_img(filepath, target_size=(64,64)))
        X_train.append(img)
        y_train.append(i)

X_train = np.asarray(X_train)
y_train = to_categorical(y_train, len(members))
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=1)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# モデルの定義
model = Sequential()
model.add(Conv2D(input_shape=X_train.shape[1:], filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256))
model.add(Activation("sigmoid"))
model.add(Dense(128))
model.add(Activation('sigmoid'))
# 分類したい人数を入れる
model.add(Dense(len(members)))
model.add(Activation('softmax'))
# コンパイル
model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

# 学習
history = model.fit(X_train, y_train, batch_size=70, epochs=1, verbose=1, validation_data=(X_test, y_test))

#モデルを保存
model_json = model.to_json()
open('YukanyaModel.json', 'w').write(model_json)
model.save_weights("YukanyaModel.h5")

# 汎化制度の評価・表示
score = model.evaluate(X_test, y_test, batch_size=32, verbose=0)
print('validation loss:{0[0]}\nvalidation accuracy:{0[1]}'.format(score))

#acc, val_accのプロット
plt.plot(history.history["acc"], label="acc", ls="-", marker="o")
plt.plot(history.history["val_acc"], label="val_acc", ls="-", marker="x")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.legend(loc="best")
plt.show()