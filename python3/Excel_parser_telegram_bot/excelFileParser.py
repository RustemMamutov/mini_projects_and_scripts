# coding: utf-8

"""
Файл содержит класс, который работает с excel файлами. Этот класс находит
выполненные задачи в листе и возвращает словарь с номерами и описанием этих
задач.
##############################################################################
The file contains class, which work with excel files. In current sheet
the class finds performed tasks and returns dictionary with tasks` numbers
and tasks` descriptions.
"""

import re

class excelFileParser:
    '''
    Класс, который занимается анализом и обработкой данных из файла .xlsx.
    ##########################################################################
    The class, which analyzes and works with data from excel file.
    '''

    def __init__(self):
        pass

    def get_ready_task_dict(self, sheet):
        '''
        Метод, который находит выполненные задачи на листе.
        ######################################################################
        The method finds performed tasks in the sheet.
        '''

        # Получение номера строки с первой задачей.
        ######################################################################
        # Getting row number with the first task.
        start_row = self.search_start_row(sheet, 1, 2, '№')
        # Получение номера строки с последней задачей.
        ######################################################################
        # Getting row number with the last task.
        end_row = self.search_finish_row(sheet, start_row, 2)
        # Цвет, которым отмечены выполненные задания.
        ######################################################################
        # Color of "ready" task.
        ready_color = str(sheet['B3'].fill.start_color.rgb)
        # Словарь, где ключи - номера строк с выполненными заданиями,
        # значения - тексты этих задач.
        ######################################################################
        # The dict, where lines` numbers are KEYS, tasks` texts are VALUES.
        result_dict = self.get_task_dict(sheet, start_row, end_row, 2, ready_color)
        return result_dict

    def get_only_today_task_dict(self, today_task_dict, yesterday_task_dict):
        '''
        Метод, который из полного списка выполненных задач удаляет те,
        которые были выполнены вчера. В итоге остаются только те задачи,
        которые были выполнены ТОЛЬКО за сегодня.
        ######################################################################
        The method deletes from today_result_dict tasks, that are in
        yesterday_task_dict. As a result, in today_result_dict will be only
        those tasks, that were done ONLY during today.
        '''

        if len(yesterday_task_dict) == 0:
            pass
        else:
            for each_key in yesterday_task_dict.keys():
                try:
                    today_task_dict.pop(each_key)
                except:
                    pass

        return today_task_dict

    def search_start_row(self, sheet_obj, row, column, text_to_find):
        '''
        Метод, который находит на данном листе номер строки с первой задачей.
        Поиск ведется по заданному символу textToFind. Находится строка,
        содержащая этот символ. Строка с первой задачей находится на 2
        позиции ниже (особенности оформления таблицы эксель).
        ######################################################################
        In current sheet the method finds the row, which contains the first
        task. The search is performed according to the specified textToFind
        symbol. The line with textToFind symbol has it`s row number. The
        row with first task is on 2 positions below (current excel table
        formatting features).
        '''

        start_row = 1
        while row <= 20:
            cellValue = sheet_obj.cell(row=row, column=column).value
            if re.search(text_to_find, str(cellValue)):
                start_row = row + 2
                break
            row += 1
        return start_row

    def search_finish_row(self, sheet_obj, row, column):
        '''
        Метод, который находит на данном листе номер строки с последней
        задачей.
        ######################################################################
        In current sheet the method finds the row, which contains the last
        task.
        '''

        while str(sheet_obj.cell(row=row, column=column).value) != 'None':
            row += 1
        return row - 1

    def get_task_dict(self, sheet_obj, start_row, end_row, column, color):
        '''
        Метод, который составляет словарь задач для данного листа (по
        переданным параметрам).
        Ключи - номера задач, значения - описание задач.
        ######################################################################
        In current sheet the method return dictionary of performed tasks.
        KEYS - tasks` numbers, VALUES - tasks` descriptions.
        '''

        i = start_row
        ready_task_dict = {}
        while i <= end_row:
            currentColor = str(sheet_obj.cell(row=i, column=column).fill.start_color.rgb)
            if currentColor == color:
                ready_task_dict[sheet_obj.cell(row=i, column = 2).value] = sheet_obj.cell(row=i, column = 4).value
            i += 1
        return ready_task_dict
