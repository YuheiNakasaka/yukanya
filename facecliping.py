import cv2
import os
import math
import numpy as np

class FaceCliping:
    def __init__(self):
        self.members = [
            "akariuemura",
            "karinmiyamoto",
            "manakainaba",
            "rurudanbara",
            "sayukitakagi",
            "tomokokanazawa",
            "yukamiyazaki"
        ]
        self.face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    
    # アメブロはメンバーを分けずに画像を取得してるので
    # member毎のディレクトリは無い
    def from_ameba_blog(self):
        dl_image_path = 'dl_images'
        face_image_path = 'face_images'
        if not os.path.exists(face_image_path):
            os.mkdir(face_image_path)

        source_images = os.listdir(dl_image_path)
        for filename in source_images:
            print(filename)
            file_path = dl_image_path + '/' + filename
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray)
            for (x,y,w,h) in faces:
                face = img[y:y+h, x:x+w]
                filename, ext = os.path.splitext(os.path.basename(file_path))
                cv2.imwrite(face_image_path + '/' + filename + '_' + str(x) + '_' + str(y) + ext, face)

    # googleから取得した画像はメンバー別に取得できてるので最初から
    # member毎のディレクトリがある
    def from_google(self):
        for member in self.members:
            dl_image_dir = 'dl_gimages'
            member_image_src_dir = dl_image_dir + '/' + member
            face_image_dir = 'face_gimages'
            if not os.path.exists(face_image_dir): os.mkdir(face_image_dir)
            member_image_dir = face_image_dir + '/' + member
            if not os.path.exists(member_image_dir):
                os.mkdir(member_image_dir)

            source_images = os.listdir(member_image_src_dir)
            for filename in source_images:
                print(filename)
                file_path = member_image_src_dir + '/' + filename
                self.detect_face_with_angle(file_path, member_image_dir)

    # 回転させながら斜め向きの顔などにも対応する
    def detect_face_with_angle(self, src_path ,output_dir):
        img = cv2.imread(src_path)
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
                faces = self.face_cascade.detectMultiScale(rotated)
                for (x, y, w, h) in faces:
                    face = rotated[y:y+h, x:x+w]
                    # cv2.imshow('face', face)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    filename, ext = os.path.splitext(os.path.basename(src_path))
                    cv2.imwrite(output_dir + '/' + filename + '_' + str(x) + '_' + str(y) + ext, face)
                if len(faces) > 0:
                    break


if __name__ == '__main__':
    client = FaceCliping()
    client.from_google()