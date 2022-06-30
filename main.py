
# пути и переменные
path1 = 'C:\\Users\\vezvi\\PycharmProjects\\ProjectOleg\\Test_folder'
path2 = 'C:\\Users\\vezvi\\PycharmProjects\\ProjectOleg\\Test_folder_copy'
path3 = 'C:\\Users\\vezvi\\PycharmProjects\\ProjectOleg\\Test_folder_brdc'

# проверка в директории файлов и копирование в другую директорию
import os
import os.path
from changing_files import *
from db_connect import *
from db_function import *
from functions import *
from dictionary import *

# список расширений для проверки
# генерация расширения вместе с требуемой датой
dif_datetime = 0
year, month, day, day_year, hour, minute, sec =  required_date(dif_datetime)
# for test
day_year = 167
hour_2 = '06'
month = '06'
day = 16
print(year, month, day, day_year, hour, '%02i' % hour )

date_ver = '010722'

str_datetime_dy = str(year) + str(day_year) + '%02i' % hour
print(str_datetime_dy)
str_datetime = str(year) + '-' + str(month) + '-' + str(day)
print(str_datetime)
fileExt = ( 'EN.rnx.gz','RN.rnx.gz','CN.rnx.gz','MN.rnx.gz','GN.rnx.gz')
print(fileExt)
#copy_ver_file(path1, path2, fileExt,str_datetime_dy)

# разархивирование
#print('unpacking_file----')
#unpacking_file2(path2)
# don't work

# 1 обработка отдельно каждой системы
# копирование по каждой системе отдельно
#
# открываем каждый файл и
#
# создаем список весов по списку скачанных файлов

# подключение к БД
cnx = connect_to_db()

#for n_sys in [1,2,3,4]:
for n_sys in [2]:
    # получение словаря весов станций
    station_heft_dict = get_dict_station_heft(cnx, path2, str_datetime, n_sys)

    # чтение файлов
    list_files = creat_selection_file(path2, station_heft_dict, n_sys)

    # сравнение данных
    list_check_data = check_data_files(list_files)

    # создание нав.файла
    brdc_datetime = datime_for_brdcfile(year, month, day, hour, minute, sec)
    creat_nav_file(list_check_data, path3, n_sys, year, day_year,brdc_datetime, date_ver)



