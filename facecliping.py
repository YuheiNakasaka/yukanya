import cv2
import os

dl_image_path = 'dl_images'
face_image_path = 'face_images'
if not os.path.exists(face_image_path):
    os.mkdir(face_image_path)

face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')

source_images = os.listdir(dl_image_path)
for filename in source_images:
    print(filename)
    file_path = dl_image_path + '/' + filename
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
        face = img[y:y+h, x:x+w]
        filename, ext = os.path.splitext(os.path.basename(file_path))
        cv2.imwrite(face_image_path + '/' + filename + '_' + str(x) + '_' + str(y) + ext, face)
