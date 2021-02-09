# coding: utf-8

'''
Функция, которая создает экземпляр класса-парсера excel и с его помощью
получает для заданного листа словарь с выполненными ТОЛЬКО ЗА СЕГОДНЯ
задачами.
##############################################################################
The function creates instance of excelFileParser.
After that the function returns dictionary with tasks, that were done
ONLY DURING TODAY.
'''

import openpyxl
from excelFileParser import excelFileParser

def maincode(partial_path, sheet_index):
    '''
    Функция, которая принимает в качестве параметра путь к папке с 2 таблицами
    и номер листа в этих таблицах, а затем функция получает для этого листа
    словарь с выполненными ТОЛЬКО ЗА СЕГОДНЯ задачами.
    ##########################################################################
    The function takes as a parameters:
    path of folder with two excel tables;
    sheet number in these excel tables.
    For the sheet the function returns dictionary with tasks, that were done
    ONLY DURING TODAY.
    '''

    # Полные пути к вчерашней и сегодняшней таблице.
    # Full paths for yesterday`s and today`s excel tables.
    yesterday_full_path = partial_path + r'/Old.xlsx'
    # today_full_path = partial_path + r'\New.xlsx'
    today_full_path = partial_path + r'/New.xlsx'

    # Создаём файлы путём открытия таблицы xlsx.
    # Вчерашняя и сегодняшняя таблица.
    ##########################################################################
    # Creating files (opening excel tables).
    # Yesterday`s and today`s tables.
    yesterday_wb = openpyxl.load_workbook(yesterday_full_path)
    today_wb = openpyxl.load_workbook(today_full_path)

    # Вчерашняя таблица. Создаём 1 лист (объект)
    # y_sheet_obj = yesterday`s Sheet Object
    y_sheet_obj = yesterday_wb.worksheets[sheet_index]

    # Сегодняшняя таблица. Создаём 1 лист (объект)
    # t_sheet_obj = today`s Sheet Object
    t_sheet_obj = today_wb.worksheets[sheet_index]

    # Создаём экземпляр класса excelFileParser.
    # Creating an instance of excelFileParser.
    my_parser = excelFileParser()

    # Вчерашняя таблица. Создаём словарь с выполненными задачами из листа.
    ##########################################################################
    # Creating a dictionary with ready tasks for yesterday excel table.
    # yrtd = yesterday ready task dict
    yrtd_dict = my_parser.get_ready_task_dict(y_sheet_obj)

    # Сегодняшняя таблица. Создаём словарь с выполненными задачами из листа.
    ##########################################################################
    # Creating a dictionary with ready tasks for today excel table.
    # trtd = today ready task dict
    trtd_dict = my_parser.get_ready_task_dict(t_sheet_obj)

    # Создаём словарь с выполненными ТОЛЬКО ЗА СЕГОДНЯ задачами из листа.
    ##########################################################################
    # Creating a dictionary with tasks, that were done ONLY DURING TODAY.
    # otrtd = only today ready task dict
    otrtd_dict = my_parser.get_only_today_task_dict(trtd_dict, yrtd_dict)

    return otrtd_dict
