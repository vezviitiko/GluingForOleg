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

def check_space(str):
    return str.replace(' ', '0')

def str_to_datetime(str):
    #print(str)
    year = check_space(str[:4])
    month = check_space(str[5:7])
    day = check_space(str[8:10])
    hour = check_space(str[11:13])
    min = check_space(str[14:16])
    sec = check_space(str[17:19])
    datetime = year+'-'+month+'-'+day+' '+hour+':'+min+':'+sec
    return datetime

def datime_for_brdcfile(year,month,day,hour,minute,sec):
    return str(str(year)[2:]+'%02i' % int(month)+'%02i' % int(day)+' %02i' % int(hour)+':%02i' % int(minute)+':%02i' % int(sec))

def check_limit_sys(line, n_sys, num_line_start_block):
    if n_sys == 1:
            if num_line_start_block < 6:
                return line
            else:
                return line[:23]+'\n'
    elif n_sys == 2:
            if num_line_start_block < 3:
                return line
            else:
                return ''
    elif n_sys == 3:
            if num_line_start_block == 4:
                if line.find('      ') > 0:
                    line.replace('                  ', '0.000000000000D+00')
                return line
            else:
                return line
    elif n_sys == 3:
            if num_line_start_block == 4:
                if line.find('      ')>0:
                    line.replace('                  ','0.000000000000D+00')
                return line
            elif num_line_start_block == 6:
                return line[:23]+'\n'
            else:
                return line
    else:
        return line

def read_file(path = os.getcwd(), filename = '', heft = 1, n_sys = 2):
    if (os.path.exists(path+'\\'+filename) and os.path.isfile(path+'\\'+filename)):
        data_file = []          #   массив блоков из файла
        data_full_block = []    #   весь блок данных
        data_num_block  = ''    #   строка численных данных
        ch_file = sys_numeric_ch_file_dict.get(n_sys)
        print('ch_file=',ch_file)
        fl_start_file = False
        with open(path+'\\'+filename) as f:
            fl_start_block = False
            num_line_start_block = 0
            for line in f:
                if fl_start_file:
                    #print(line)
                    if line[:1]==ch_file:
                        if fl_start_block:
                            data_num_block = data_num_block.replace('E', 'D')
                            data_num_block = data_num_block.replace('e', 'D')
                            data_full_block.append(data_num_block)
                            data_full_block.append(False)
                            data_file.append(data_full_block)
                            #print(data_full_block)
                            data_full_block = []
                            data_num_block = ''
                            num_line_start_block = 0

                        #line = check_space(line)
                        fl_start_block = True
                        data_full_block.append(check_space(line[:3]))       # спутник
                        data_full_block.append(str_to_datetime(line[4:23])) # время
                        data_full_block.append(heft)                        # вес
                        #print(line[:23])
                        data_num_block += line[23:]                         # данные

                    elif fl_start_block:
                        #print(len(line), line)
                        data_num_block += check_limit_sys(line, n_sys, num_line_start_block)
                        num_line_start_block += 1

                elif line.find('END OF HEADER')>0:
                    fl_start_file = True

            data_num_block = data_num_block.replace('E', 'D')
            data_num_block = data_num_block.replace('e', 'D')
            data_full_block.append(data_num_block)
            data_full_block.append(False)
            data_file.append(data_full_block)

    print(data_file)
    if data_file:
        return data_file

def creat_selection_file(path = os.getcwd(), station_heft_dict = {}, n_sys = 2):
    print('creat_selection_file ----')
    search_ext = sys_numericfilename_dict.get(n_sys)
    print(search_ext)

    list_files = []
    # cтруктура
    #   = [['Name station', 'datatime', heft, str_num_data], [..],...]
    #
    if (os.path.exists(path) and os.path.isdir(path)):
        for filename in os.listdir(path):
            if filename.find(search_ext)>0:
                print('file=',filename)
                heft = station_heft_dict.get(filename[:4])
                print('heft=', heft)
                if heft is None:
                    heft = 1
                data = read_file(path, filename, heft, n_sys)
                if data is not None:
                    list_files.append(data)
                print('list_files = ', list_files)

    if list_files:
        return list_files

def check_duplicate_data(list_data = []):
    arr_pop = []
    for i, data_block1 in enumerate(list_data):
        for j, data_block2 in enumerate(list_data[i+1:]):
            if data_block1[1] == data_block2[1] \
                and data_block1[0] == data_block2[0]:
                    print(data_block1[0], data_block1[1], data_block1[2], data_block2[2])
                    if data_block1[2] >= data_block2[2]:
                        arr_pop.append(i+1 + j)
                        print(i+1 + j)
                    else:
                        arr_pop.append(i)

    print('arr_pop = ', arr_pop)
    arr_pop = list(set(arr_pop)) # убираем дублируемые
    print('arr_pop = ', arr_pop)
    for i in reversed(arr_pop):
        list_data.pop(i)

    return list_data

def check_data_files2(list_files):
    print('check_data_files2 ----')
    list_check_data = []
    for file_ in list_files:
        for data_block in file_:
            list_check_data.append(data_block)

    for i in range(len(list_check_data)-1):
        for j in range(i+1, len(list_check_data)):
            if list_check_data[i][0] == list_check_data[j][0] \
                and list_check_data[i][1] == list_check_data[j][1]:
                    #and list_check_data[i][4] == False \
                    #and list_check_data[j][4] == False:
                print('==========Нашел=============')
                print(list_check_data[i][0], list_check_data[i][1], list_check_data[i][2],
                      list_check_data[j][0], list_check_data[j][1], list_check_data[j][2])
                if list_check_data[i][3] == list_check_data[j][3]:  # сравнение значений
                    print('==========Ideal=============')
                    list_check_data[i][2] = list_check_data[i][2] + list_check_data[j][2]
                    #list_check_data[j][4] = True
                    print(list_check_data[i])

                print('SIZE = ===', len(list_check_data))

    #print('list_check_data=', list_check_data)

    # убираем дубликаты
    list_check_data = check_duplicate_data(list_check_data)

    if list_check_data:
        return list_check_data

def check_data_files(list_files):
    print('check_data_files ----')
    list_check_data = []

    for file_ in list_files:
        for data_block_file_ in file_:
            flag_check = False
            print(0, data_block_file_[1])
            for data_block1 in list_check_data:
                print(1)
                if data_block1[1] == data_block_file_[1] \
                            and data_block1[0] == data_block_file_[0]:
                    flag_check = True
                    print('==========Нашел=============')
                    print(data_block1[0], data_block1[1], data_block1[2],
                          data_block_file_[0], data_block_file_[1], data_block_file_[2])
                    if data_block1[3] == data_block_file_[3]:  # сравнение значений
                        print('==========Ideal=============')
                        data_block1[2] = data_block1[2] + data_block_file_[2]
                        print(data_block1)
                    else:
                        print("NO ================")
                        list_check_data.append(data_block_file_)
                    print('SIZE = ===', len(list_check_data))
                    print(2)
            if  flag_check == False:
                print("ADD NEW DATA ================")
                print(data_block_file_)
                list_check_data.append(data_block_file_)

    print('list_check_data=',list_check_data)

    # убираем дубликаты
    list_check_data = check_duplicate_data(list_check_data)

    if list_check_data:
        return list_check_data

def creat_nav_file(list_check_data, path = os.getcwd(), n_sys = 1, year = '2022', day_year = '001', brdc_datetime = '', date_ver = '010122'):
    print('     creat_nav_file')
    ch_brdc = brdc_alphanumeric_dict.get(n_sys)
    print('Brdc{0}0.{1}{2}'.format(str(day_year), str(year)[2:], ch_brdc))
    f = open(path + '\\' + 'Brdc{0}0.{1}{2}'.format(day_year, str(year)[2:],ch_brdc), 'w')

    s1 = "     3.02            N:GNSS NAV DATA    R: {0}RINEX VERSION / TYPE\n" \
         "Версия от {1}                          {2}UTCPGM / RUN BY / DATE\n" \
         "GLUT  0.6053596735D-08 0.000000000D+00      0    0          TIME SYSTEM CORR\n" \
         "                                                            END OF HEADER\n".format( sys_alphafullnumeric_dict.get(n_sys), date_ver, brdc_datetime)
    f.write(s1)


    # сортировка
    from operator import itemgetter
    list_check_data = sorted(sorted(list_check_data, key=lambda x:x[0]), key=lambda x:x[1])

    for data_block in list_check_data:
        #print(data_block[0] +' '+ str(data_block[1]).replace('-', ' ').replace(':', ' '))
        #print(data_block)
        f.write((data_block[0] +' '+ str(data_block[1]).replace('-', ' ').replace(':', ' ')))
        f.write(data_block[3])
    f.close()
