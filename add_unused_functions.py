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
