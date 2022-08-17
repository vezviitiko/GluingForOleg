#!/usr/bin/python3
#coding=UTF-8
__autor__ = 'KomissarovAV'

import os.path
import io

def create_log_file(path, name_log_file):
    print(path)
    print(os.path.isdir(path))
    if (os.path.exists(path) and os.path.isdir(path)):
        f = io.open(path + '\\' + name_log_file, 'a', 1, encoding='utf-8')
        print('log-file create')
        return f
    else:
        print('error log-file create')
        return 0
