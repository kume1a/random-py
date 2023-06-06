# -*- coding: utf-8 -*-

import os

loc = ""

def count_lines(file_path):
	with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
		return len(f.readlines())

folder_count,file_count,line_count = 0,0,0
for e in os.walk(loc):
    current_dir,dirs,files = e
    folder_count += len(dirs)
    for file in files:
        if not file.endswith(".g.dart") and not file.endswith('.freezed.dart') and not file.endswith('.config.dart'):
        	file_count += 1
        	line_count += count_lines(f'{current_dir}/{file}')

print(f'file count = {file_count}')
print(f'folder count = {folder_count}')
print(f'line count = {line_count}')
