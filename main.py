
# пути и переменные
path1 = 'C:\\Users\\vezvi\\PycharmProjects\\ProjectOleg\\Test_folder'
path2 = 'C:\\Users\\vezvi\\PycharmProjects\\ProjectOleg\\Test_folder_copy'

# проверка в директории файлов и копирование в другую директорию
import os
import os.path
from function import *
from db_connect import *
from db_function import *
from read_file import *

# список расширений для проверки
# генерация расширения вместе с требуемой датой
dif_datetime = 0
year, month, day, day_year, hour, hour_2 =  required_date(dif_datetime)
# for test
day_year = 167
hour_2 = '06'
month = '06'
day = 16
print(year, month, day, day_year, hour, hour_2 )

str_datetime_dy = str(year) + str(day_year) + hour_2
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

# получение словаря весов станций
station_heft_dict = get_dict_station_heft(cnx, path2, str_datetime)

# чтение файлов
list_files = creat_selection_file(path2, station_heft_dict)

# сравнение данных
list_check_data = check_data_files(list_files)


