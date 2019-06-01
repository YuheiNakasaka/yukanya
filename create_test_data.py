import shutil
import random
import os
import re

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
    member_dir = member_image_dir + '/' + member + '/'
    member_files = os.listdir(member_dir)
    random.shuffle(member_files)
    test_dir = 'test' + '/' + member
    os.makedirs(test_dir, exist_ok=True)
    for t in range(len(member_files) // 5):
        if not re.match('.+.jpg', member_files[t]): continue
        shutil.move(member_dir + member_files[t], test_dir)