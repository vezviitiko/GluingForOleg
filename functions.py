__autor__ = 'KomissarovAV'

import os
from dictionary import *

def required_date(dif_datetime = 0):
    import datetime
    now = datetime.datetime.now()
    now = now - datetime.timedelta(dif_datetime)
    year = now.year
    month = '%02i' % now.month
    day = now.day
    day_year = now.strftime('%j')
    hour = now.hour
    hour_2 = '%02i' % hour
    minute = now.minute
    sec = now.second
    return year, month, day, day_year, hour, minute, sec

def check_space(str, pos):
    if str[pos]==' ':
        str[pos]=0
    return str

def str_to_datetime(str):
    year = check_space(str[:4],1)
    month = check_space(str[5:7], 0)
    day = check_space(str[8:10], 0)
    hour = check_space(str[11:13], 0)
    min = check_space(str[14:16], 0)
    sec = check_space(str[17:19], 0)
    datetime = year+'-'+month+'-'+day+' '+hour+':'+min+':'+sec
    return datetime

def datime_for_brdcfile(year,month,day,hour,minute,sec):
    return str(str(year)[2:]+'%02i' % int(month)+'%02i' % int(day)+' %02i' % int(hour)+':%02i' % int(minute)+':%02i' % int(sec))

def str_to_num(str):
    return float(str)

def line_str_to_num(line,data_num_block):
    for str_num in line.split():
        if len(str_num) > 20:
            num_zn = str_num[18:].find('-')
            str_num_1 = str_num[:18+num_zn]
            data_num_block.append(str_to_num(str_num_1))
            str_num_2 = str_num[18+num_zn:]
            data_num_block.append(str_to_num(str_num_2))
        else:
            data_num_block.append(str_to_num(str_num))

def read_file(path = os.getcwd(), filename = '', heft = 0, n_sys = 2):
    if (os.path.exists(path+'\\'+filename) and os.path.isfile(path+'\\'+filename)):
        data_file = []          # массив блоков из файла
        data_full_block = []    # весь блок данных
        data_num_block = []     # блок численных данных
        ch_file = sys_numeric_ch_file_dict.get(n_sys)
        print('ch_file=',ch_file)
        with open(path+'\\'+filename) as f:
            fl_start_block = False
            for line in f:
                if line[:1]==ch_file:
                    if fl_start_block:
                        data_full_block.append(data_num_block)
                        data_file.append(data_full_block)
                        data_full_block = []
                        data_num_block = []

                    line = check_space(line, 1)
                    fl_start_block = True
                    data_full_block.append(line[:3])                    # спутник
                    data_full_block.append(str_to_datetime(line[4:23])) # время
                    data_full_block.append(heft)                        # вес

                    line = line.strip(line[:23])             # далее данные
                    line_str_to_num(line,data_num_block)

                elif fl_start_block:
                    line_str_to_num(line, data_num_block)

    print(data_file)
    if data_file:
        return data_file

def creat_selection_file(path = os.getcwd(), station_heft_dict = [], n_sys = 2):
    print('creat_selection_file ----')
    search_ext = sys_numericfilename_dict.get(n_sys)
    print(search_ext)

    list_files = []
    # cтруктура
    #   = [['Name station', 'datatime', heft, [array]], [..],...]
    #
    if (os.path.exists(path) and os.path.isdir(path)):
        for filename in os.listdir(path):
            if filename.find(search_ext)>0:
                print('file=',filename)
                heft = station_heft_dict.get(filename[:4])
                print('heft=', heft)
                data = read_file(path, filename, heft, n_sys)
                if data is not None:
                    list_files.append(data)
                print(list_files)

    if list_files:
        return list_files

def check_duplicate_data(list_data = []):
    arr_pop = []
    for i, data_block1 in enumerate(list_data):
        for j, data_block2 in enumerate(list_data):
            if i != j \
                and data_block1[1] == data_block2[1] \
                and data_block1[0] == data_block2[0]:
                    if data_block1[3] > data_block2[3]:
                        arr_pop.append(j)
                    else:
                        arr_pop.append(i)

    for i in reversed(arr_pop):
        list_data.pop(i)
    return list_data

def check_data_files(list_files):
    print('check_data_files ----')
    list_check_data = list_files[0] # МАССИВ ПРОВЕРЕННЫХ
    print(list_check_data)

    for data_block1 in list_check_data:
        for file_ in list_files:
            if list_check_data != file_:    # не берем первый
                for data_block2 in file_:
                    if data_block1[1] == data_block2[1] \
                            and data_block1[0] == data_block2[0]:
                        print('==========Нашел=============')
                        print(data_block1[0], data_block1[1], data_block1[2],
                              data_block2[0], data_block2[1], data_block2[2])

                        if data_block1[3] == data_block2[3]:  # сравнение значений
                            print('==========Ideal=============')
                            data_block1[2] = data_block1[2] + data_block2[2]
                            print(data_block1)
                        else:
                            print("NO ================")
                            list_check_data.append(data_block2)

    print(list_check_data)

    # убираем дубликаты
    list_check_data = check_duplicate_data(list_check_data)

    if list_check_data:
        return list_check_data

def creat_nav_file(list_check_data, path = os.getcwd(), n_sys = 1, year = '2022', day_year = '001', brdc_datetime = '', date_ver = ''):
    ch_brdc = brdc_alphanumeric_dict.get(n_sys)
    print('Brdc{0}0.{1}{2}'.format(str(day_year), str(year)[2:], ch_brdc))
    f = open(path + '\\' + 'Brdc{0}0.{1}{2}'.format(day_year, str(year)[2:],ch_brdc), 'w')

    s1 = "     3.02            N:GNSS NAV DATA    R: {0}RINEX VERSION / TYPE\n" \
         "Версия от {1}                          {2}UTCPGM / RUN BY / DATE\n" \
         "GLUT  0.6053596735D-08 0.000000000D+00      0    0          TIME SYSTEM CORR\n" \
         "                                                            END OF HEADER\n".format( sys_alphafullnumeric_dict.get(n_sys), date_ver, brdc_datetime)
    f.write(s1)
    for data_block in list_check_data:
        print(data_block[0] +' '+ str(data_block[1]).replace('-', ' ').replace(':', ' '))
        print(data_block)
        f.write((data_block[0] +' '+ str(data_block[1]).replace('-', ' ').replace(':', ' ')))
        for i, elem in enumerate(data_block[3]):
            if int(elem)>0:
                f.write(' ' + str(elem))
            else:
                f.write(' ' + str(elem))
            print(elem)
    f.close()
