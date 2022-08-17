#!/usr/bin/python3
#coding=UTF-8
__autor__ = 'KomissarovAV'

import psycopg2
import os
from configparser import ConfigParser

def read_db_config(filename='config.ini',section='postgresql'):

    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def connect_to_db(path = os.getcwd(), filename='config.ini', section='postgresql'):

    try:
        print(path + '\\' + filename)
        if (os.path.exists(path + '\\' + filename)
                and os.path.isfile(path + '\\' + filename)):
            db_config = read_db_config(filename,section)
            cnx = psycopg2.connect(**db_config)

            return cnx
        else:
            raise Exception('not found file db config')
            exit(1)
    except:
        raise Exception('db not connected')
        exit(1)

