#!/usr/bin/python3
#coding=UTF-8
__autor__ = 'KomissarovAV'

import gzip



import shutil
def copy_file(path_from, path_to, file):
    shutil.copy(path_from + '\\' + file, path_to + '\\' + file)

def remove_file_dir(path):
    if (os.path.exists(path) and os.path.isdir(path)):
        for file_ in os.listdir(path):
            os.remove('{0}\\{1}'.format(path, file_))

def copy_file_for_list(path_from, path_to, file_list):
    for file_ in file_list:
        if os.path.isfile(path_from + '\\' + file_):
            copy_file(path_from, path_to, file_)

def copy_ver_file(path_from, path_to, fileExt, str_datetime):
    # список файлов на копирование
    file_list = [_ for _ in os.listdir(path_from) if _.endswith(fileExt)]
    file_list_ver = []
    # проверка файлов на время в названии файлов
    for file_ in file_list:
        if file_[12:21] == str_datetime:
            file_list_ver.append(file_)
    print(file_list_ver)
    copy_file_for_list(path_from, path_to, file_list_ver)

import os
import gzip
import shutil

def opener(filename):
    f = open(filename,'rb')
    if (f.read(2) == '\x1f\x8b'):
        f.seek(0)
        return gzip.GzipFile(fileobj=f)
    else:
        f.seek(0)
        return f

def unpacking_file(path):
    print(1)
    if (os.path.exists(path) and os.path.isdir(path)):
        print(2)
        for file_ in os.listdir(path):
            print(file_)
            if file_.endswith('gz') or file_.endswith('GZ'):
                print('{0}\\{1}'.format(path, file_))
                print('{0}\\{1}'.format(path, file_[:-3]))
                with opener('{0}\\{1}'.format(path, file_)) as f_in:
                    with open('{0}\\{1}'.format(path, file_[:-3]), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(3)
                os.remove('{0}\\{1}'.format(path, file_))
                print(4)

def unpacking_file2(path):
    print(1)
    if (os.path.exists(path) and os.path.isdir(path)):
        print(2)
        for file_ in os.listdir(path):
            print(file_)
            if file_.endswith('gz') or file_.endswith('GZ'):
                print('{0}\\{1}'.format(path, file_))
                print('{0}\\{1}'.format(path, file_[:-3]))
                inFile = gzip.open('{0}\\{1}'.format(path, file_), 'rb')
                str_file = inFile.read()
                inFile.close()
                open('{0}\\{1}'.format(path, file_[:-3]), 'wb').write(str_file)
                print(3)
                os.remove('{0}\\{1}'.format(path, file_))
                print(4)