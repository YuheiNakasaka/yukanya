import numpy as np
import math
import cv2
import sys
import re
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt
import requests

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
    if not (len(sys.argv) == 3 and re.match('.+\.(jpg|jpeg|png)', sys.argv[1])):
        print('Error: set image path or set (local or api) mode')
        return False

    mode = sys.argv[2]
    img_path = sys.argv[1]
    model_path = "YukanyaModel_vgg_all.h5"
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
    face_data = []
    img = cv2.imread(img_path)
    if img is not None:
        rows, cols, colors = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hypot = int(math.hypot(rows, cols))
        frame = np.zeros((hypot, hypot), np.uint8)
        frame[int((hypot - rows) * 0.5):int((hypot + rows) * 0.5), int((hypot - cols) * 0.5):int((hypot + cols) * 0.5)] = gray
        # 正面が一番多いので最初に試す。10や-10は正面と似たようなもんなので無駄に同じような画像が検出されてしまうから最後。
        for deg in [0, 50, -50, -40, 40, -30, 30, -20, 20, -10, 10]:
            matrix = cv2.getRotationMatrix2D((hypot * 0.5, hypot * 0.5), -deg, 1.0)
            rotated = cv2.warpAffine(frame, matrix, (hypot, hypot))
            faces = face_cascade.detectMultiScale(rotated)
            for (x, y, w, h) in faces:
                face = rotated[y:y+h, x:x+w]
                face = cv2.resize(face, (64, 64))
                face_data.append(face)

    print('Face: ', len(face_data))
    if mode == 'api':
        print('API mode')
        # grayscaleを3チャンネルへ
        face_img = face_data[0]
        org = np.dstack((face_img, face_img))
        org = np.dstack((org, face_img))
        face_img = org

        data = {
            'images': face_img.tolist()
        }
        API_URL = 'http://localhost:8080' #'https://rocky-sands-87995.herokuapp.com/'
        res = requests.post(API_URL, json=data)
        json = res.json()
        pred = json.get('data')
        print(pred)
    else:
        print('local mode')
        for face_img in face_data[:1]:
            # grayscaleを3チャンネルへ
            org = np.dstack((face_img, face_img))
            org = np.dstack((org, face_img))
            face_img = org

            img_list = []
            img_list.append(img_to_array(face_img) / 255)
            img_list = np.array(img_list, dtype=np.float32)

            model = load_model(model_path)
            y_pred = model.predict(img_list)
            sorted_results = []
            for i, score in enumerate(y_pred[0]):
                sorted_results.append([score *  100, member_to_name(label[i])])
            sorted_results.sort()
            for result in sorted_results[::-1]:
                print(result[1] + ': ' + str(result[0]) + '%')

if __name__ == '__main__':
    main()