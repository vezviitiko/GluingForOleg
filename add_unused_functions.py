#!/usr/bin/python3
#coding=UTF-8
__autor__ = 'KomissarovAV'

def str_to_num(str):
    return float(str)

def line_str_to_num(line,data_num_block):
    print('line_str_to_num   ')
    for str_nums in line.split():
        if len(str_nums) > 20:
            str_num = ''
            i = 0
            while i < len(str_nums):
                num_zn = str_nums[18+i:].find('-')
                if num_zn < 0:
                    num_zn = str_nums.rfind('-')
                    str_num = str_nums[num_zn:]
                    break
                str_num = str_nums[:18+i + num_zn]
                data_num_block.append(str_to_num(str_num))
                i+=18+num_zn
            data_num_block.append(str_to_num(str_num))

        else:
            data_num_block.append(str_to_num(str_nums))

def check_data_files(list_files, f_log):
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
    list_check_data = check_duplicate_data(list_check_data, f_log)

    if list_check_data:
        return list_check_data
