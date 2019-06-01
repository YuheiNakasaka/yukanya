import numpy as np
import cv2
import os
import re
from scipy import ndimage

def create_angle_image(img, base_membar_dir, basename, ext, suffix):
    for angle in [-10, 0, 10]:
        # 回転
        rotate_img = ndimage.rotate(img, angle)
        angle_file_path = os.path.join(base_membar_dir, basename + '_' + str(angle) + '_' + suffix + ext)
        cv2.imwrite(angle_file_path, rotate_img)
        # 閾値
        threshold_img = cv2.threshold(rotate_img, 100, 255, cv2.THRESH_TOZERO)[1]
        threshold_file_path = os.path.join(base_membar_dir, basename + '_' + str(angle) + '_' + suffix + '_' + 'threshold' + ext)
        cv2.imwrite(threshold_file_path, threshold_img)
        # Gaussian
        gaussian_img = cv2.GaussianBlur(rotate_img, (5, 5), 0)
        gaussian_file_path = os.path.join(base_membar_dir, basename + '_' + str(angle) + '_' + suffix + '_' + 'gaussian' + ext)
        cv2.imwrite(gaussian_file_path, gaussian_img)

members = [
  "akariuemura",
  "karinmiyamoto",
  "manakainaba",
  "rurudanbara",
  "sayukitakagi",
  "tomokokanazawa",
  "yukamiyazaki"
]
member_image_dir = "members"

for member in members:
  print(member)
  base_membar_dir = member_image_dir + '/' + member
  for filename in os.listdir(base_membar_dir):
      if not re.match('.+_\d+_\d+\.jpg', filename): continue
      basename, ext = os.path.splitext(filename)
      filepath = base_membar_dir + '/' + filename
      img = cv2.imread(filepath)

      # コントラスト調整
      min_table = 50
      max_table = 205
      diff_table = max_table - min_table
      LUT_HC = np.arange(256, dtype = 'uint8' )
      LUT_LC = np.arange(256, dtype = 'uint8' )
      for i in range(0, min_table):
          LUT_HC[i] = 0
      for i in range(min_table, max_table):
          LUT_HC[i] = 255 * (i - min_table) / diff_table
      for i in range(max_table, 255):
          LUT_HC[i] = 255
      for i in range(256):
          LUT_LC[i] = min_table + i * (diff_table) / 255
      high_cont_img = cv2.LUT(img, LUT_HC)
      low_cont_img = cv2.LUT(img, LUT_LC)
      high_cont_file_path = os.path.join(base_membar_dir, basename + '_highcont' + ext)
      cv2.imwrite(high_cont_file_path, high_cont_img)
      low_cont_file_path = os.path.join(base_membar_dir, basename + '_lowcont' + ext)
      cv2.imwrite(low_cont_file_path, low_cont_img)

      # 左右反転
      hflip_img = cv2.flip(img, 1)
      flip_file_path = os.path.join(base_membar_dir, basename + '_flip' + ext)
      cv2.imwrite(flip_file_path, hflip_img)

      # 回転版
      create_angle_image(img, base_membar_dir, basename, ext, 'normal')
      create_angle_image(hflip_img, base_membar_dir, basename, ext, 'hflip')
      create_angle_image(high_cont_img, base_membar_dir, basename, ext, 'highcont')
      create_angle_image(low_cont_img, base_membar_dir, basename, ext, 'lowcont')
