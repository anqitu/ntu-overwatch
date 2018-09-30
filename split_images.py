import os
import glob
import pandas as pd
from shutil import copyfile
from sklearn.model_selection import train_test_split

original_directory = './cam_images/'
saved_directory = './cam_images_label/'

image_paths = glob.glob(original_directory + "*/*.jpg")
images_df = pd.DataFrame(image_paths, columns = ['original_path'])
images_df['location'] = images_df['original_path'].apply(lambda path: path.split('/')[2])
images_df['date'] = images_df['original_path'].apply(lambda path: '-'.join(path.split('/')[3].split('.')[0].split('-')[:3]))
images_df['time'] = images_df['original_path'].apply(lambda path: '-'.join(path.split('/')[3].split('.')[0].split('-')[3:]))
images_df['hour'] = images_df['original_path'].apply(lambda path: path.split('/')[3].split('.')[0].split('-')[3])

images_df.head()

os.makedirs(saved_directory)

people = ['anqi', 'mengyang', 'eva', 'kexin', 'weihong']
for person in people:
    os.makedirs(os.path.join(saved_directory, person))
    for location in images_df['location'].unique():
        os.makedirs(os.path.join(saved_directory, person, location))

for location in images_df['location'].unique():
    location_df = images_df[images_df['location'] == location]
    unkept_df, kept_df = train_test_split(location_df, test_size = 100, stratify = location_df['hour'])
    for i in range(5):
        for index, row in kept_df.iloc[i * 20 : i * 20 +20].iterrows():
            copyfile(row['original_path'], os.path.join(saved_directory, people[i], location, os.path.basename(row['original_path'])))
