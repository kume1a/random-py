#!python3
# -*- coding: utf-8 -*-
import os
import zipfile


def deleteFiles(path, delete=False, extensions=['.srt', '.vtt', '.url']):
    os.chdir(path)
    for folder in os.listdir('.'):
        try:
            os.chdir(folder)
        except NotADirectoryError as err:
            print(err)
            continue
        for f in os.listdir('.'):
            if any([f.endswith(extension) for extension in extensions]):
                print(f)
                try:
                    if delete:
                        os.remove(f)
                except Exception as err:
                    print(err)
                    continue
        os.chdir("..")

def unzipFiles(path):
    os.chdir(path)
    for folder in os.listdir():
        try:
            os.chdir(folder)
        except NotADirectoryError as err:
            print(err)
            continue
        for file in os.listdir():
            if file.endswith(".zip"):
                print("deleting: {}".format(file))
                os.remove(file)
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(file[:-8])
        os.chdir("..")

if __name__=="__main__":
    location = ""
    deleteFiles(path=location, delete=True, extensions=['.html', '.zip', '.txt'])










