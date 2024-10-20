# -*- coding: utf-8 -*-

import os

def count_files_in_folder(path):
  folder_count, file_count, line_count = 0, 0, 0

  for e in os.walk(path):
    current_dir, dirs, files = e
    folder_count += len(dirs)
    for file in files:
      if not file.endswith(".g.dart") and not file.endswith('.freezed.dart') and not file.endswith('.config.dart'):
        file_count += 1
        line_count += count_lines(f'{current_dir}/{file}')
  
  
  print(f'file count = {file_count}')
  print(f'folder count = {folder_count}')
  print(f'line count = {line_count}')
  print('')

def count_lines(file_path):
  with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    return len(f.readlines())

count_files_in_folder('C:/Users/Toko/Dev/projects/sonify/sonify/packages/sonify_client/lib')
count_files_in_folder('C:/Users/Toko/Dev/projects/sonify/sonify/packages/sonify_storage/lib')
count_files_in_folder('C:/Users/Toko/Dev/projects/sonify/sonify/packages/domain_data/lib')
count_files_in_folder('C:/Users/Toko/Dev/projects/sonify/sonify/lib')
