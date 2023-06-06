import os
import csv
import shutil


def get_csv_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        return list(reader)


def unpack_list(l):
    return [j for i in l for j in i]


def image_exists(in_images, image_name):
    for name in in_images:
        if name.endswith(image_name):
            return True
    return False


PATH = ''
print(os.listdir(PATH))

creation_images = unpack_list(get_csv_data('../../image_paths/creation_images.csv'))
author_images = unpack_list(get_csv_data('../../image_paths/author_images.csv'))

# for file in os.listdir(PATH):
#     if file.endswith('.mp3'):
#         continue
#
#     if not image_exists(creation_images, file) and not image_exists(author_images, file):
#         shutil.move(f'{PATH}/{file}', f'./unused_images/{file}')
#         print(file)
