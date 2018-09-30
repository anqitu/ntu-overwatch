import os
import glob
from datetime import datetime, timedelta

directory = './cam_images/'
image_paths = glob.glob(directory + "*/*.jpg")
for original_path in sorted(image_paths)[::-1]:
    original_time = original_path.split('/')[3].split('.')[0]
    actual_time = (datetime.strptime(original_time, '%Y-%m-%d-%H-%M-%S') + timedelta(hours=8)).strftime('%Y-%m-%d-%H-%M-%S')
    actual_path = original_path.replace(original_time, actual_time)
    os.rename(original_path, actual_path)
