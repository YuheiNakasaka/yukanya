import cv2
import numpy as np
import os
import re
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical
from keras.layers import Activation, Dense, Dropout, Flatten, Input
from keras.models import Sequential, Model
from keras.preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split
from keras.applications.vgg19 import VGG19

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
n_category = len(members)

# 訓練データ
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

X_train = np.asarray(X_train).astype('float32') / 255.0
y_train = to_categorical(y_train, n_category)
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=1)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# モデルの定義: VGG19モデル
input_tensor = Input(shape=(64,64,3))
vgg19_model = VGG19(include_top=False, weights='imagenet', input_tensor=input_tensor)

top_model = Sequential()
top_model.add(Flatten(input_shape=vgg19_model.output_shape[1:]))
top_model.add(Dense(256))
top_model.add(Activation("sigmoid"))
top_model.add(Dropout(0.5))
top_model.add(Dense(128))
top_model.add(Activation('sigmoid'))
top_model.add(Dense(n_category))
top_model.add(Activation("softmax"))

model = Model(input=vgg19_model.input, output=top_model(vgg19_model.output))

for layer in model.layers[:17]:
    layer.trainable = False

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
model.summary()

# 学習
history = model.fit(X_train, y_train, batch_size=100, epochs=50, verbose=1, validation_data=(X_test, y_test))

#モデルを保存
model.save("YukanyaModel_vgg_all.h5")
model_json = model.to_json()
open('YukanyaModel_vgg.json', 'w').write(model_json)
model.save_weights("YukanyaModel_vgg.h5")

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