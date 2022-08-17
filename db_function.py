#!/usr/bin/python3
#coding=UTF-8
__autor__ = 'KomissarovAV'

import os
def set_station(path):
    return set([_[:4] for _ in os.listdir(path) if _[:4].isalpha()])

def create_dict_from_list(list_station):
    return dict.fromkeys(list_station, 0)

def dict_station(path):
    return create_dict_from_list(list_station(path))

def get_dict_station_heft(cnx, path, str_datetime, n_sys = 1):
    print('get_heft')
    cursor = cnx.cursor()
    print(str_datetime)
    set_station_ = set_station(path)
    print(set_station_)
    station_list = []
    heft_list = []
    print(''' Select a1.ps_sp3, COALESCE(a2.heft,0) from ps_heft_sp3 a1
                        left OUTER join ps_heft_sp3 a2
                            on a1.ps_sp3 = a2.ps_sp3
                            and a2.epoch = '{0}' and a2.n_sys = {2}
                            where a1.ps_sp3 in {1} 
                '''.format(str_datetime, tuple(set_station_), n_sys))
    cursor.execute(''' Select a1.ps_sp3, COALESCE(a2.heft,0) from ps_heft_sp3 a1
                        left OUTER join ps_heft_sp3 a2
                            on a1.ps_sp3 = a2.ps_sp3
                            and a2.epoch = '{0}' and a2.n_sys = {2}
                            where a1.ps_sp3 in {1} 
                '''.format(str_datetime, tuple(set_station_), n_sys))
    for row in cursor:
        print(row)
        station_list.append(row[0])
        heft_list.append(row[1])

    station_heft_dict = dict(list(zip(station_list, heft_list)))
    print(station_heft_dict)
    return station_heft_dict