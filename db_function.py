__autor__ = 'KomissarovAV'

import os
def set_station(path):
    return set([_[:4] for _ in os.listdir(path)])

def create_dict_from_list(list_station):
    return dict.fromkeys(list_station, 0)

def dict_station(path):
    return create_dict_from_list(list_station(path))

def get_dict_station_heft(cnx, path, str_datetime):
    print('get_heft')
    cursor = cnx.cursor()
    print(str_datetime)
    set_station_ = set_station(path)
    station_list = []
    heft_list = []
    print(''' Select ps_sp3, heft from ps_heft_sp3
                        where epoch = '{0}' and ps_sp3 in {1}
                '''.format(str_datetime, tuple(set_station_)))
    cursor.execute(''' Select ps_sp3, heft from ps_heft_sp3
                        where epoch = '{0}' and ps_sp3 in {1}
                '''.format(str_datetime, tuple(set_station_)))
    for row in cursor:
        station_list.append(row[0])
        heft_list.append(row[1])

    station_heft_dict = dict(list(zip(station_list, heft_list)))

    print(station_heft_dict)
    return station_heft_dict



