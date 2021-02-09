"""
Эта программа производит поиск файлов с заданным расширением
(список FILE_NAME_EXTENSION_LIST) в указанной папке.
В файлах с расширением .cpp, .h, .c, .asm, .py программа
считает количествово строк кода.
Результат выводится в файле excel.
#################################################################
The program searches files with certain extension
(FILE_NAME_EXTENSION_LIST) in certain folder.
In files .cpp, .h, .c, .asm, .py the program
calculates count lines of code.
The result outputs in excel file.
"""

import os
import re
import time
import xlsxwriter
import inspect


# FILE_NAME_EXTENSION_LIST = ['.CPP', '.H', '.C', '.BPG', '.BPR',
# '.HPP', '.PRO', '.ASM', '.HEX', '.EEP', '.EXE', '.DLL']
FILE_NAME_EXTENSION_LIST = ['.CPP', '.H', '.C', '.BPG', '.BPR',
                            '.HPP', '.PRO', '.ASM', '.HEX', '.EEP',
                            '.EXE', '.DLL', '.PY']
ENCODINGS_LIST = ["UTF8", "ASCII", "cp1251", "CP866"]


class CodeLineChecker:
    """
    Класс, содержащий набор функций, проверяющих является ли строка кодом
    #################################################################
    The class contains methods, which check the string is code or not
    """

    def __init__(self):
        pass

    def clc_check_py(self, string):
        """
        В файле .py метод проверяет является ли строка кодом.
        По умолчанию строка считается кодом (flag = True).
        #################################################################
        In .py file the method checks the line is code or not.
        By default the string is considered as a code (flag = True).
        """
        flag = True
        # Поиск в начале строки (либо после нескольких пробелов) символа '#'.
        # Searching the character '#' at the beginning of the line or after several spaces from beginning.
        if re.search(r'^\s*#.*$', string):
            flag = False
        # Поиск пустой строки. Такая строка считается комментарием (flag = False).
        # Searching empty line. The line is considered as a comment (flag = False).
        elif re.search(r'^\s*$', string):
            flag = False
        else:
            pass
        return flag

    def clc_check_c_cpp_h(self, string):
        """
        В файле .c; .cpp; .h метод проверяет является ли строка кодом.
        По умолчанию строка считается кодом (flag = True).
        #################################################################
        In .c; .cpp; .h file the method checks the line is code or not.
        By default the string is considered as a code (flag = True).
        """
        flag = True
        # Поиск в начале строки (либо после нескольких пробелов) символа '/'.
        # Searching the character '/' at the beginning of the line or after several spaces from beginning.
        if re.search(r'^\s*/.*$', string):
            flag = False
        # Поиск пустой строки. Такая строка считается комментарием (flag = False).
        # Searching empty line. The line is considered as a comment (flag = False).
        elif re.search(r'^\s*$', string):
            flag = False
        return flag

    def clc_check_asm(self, string):
        """
        В файле .asm метод проверяет является ли строка кодом.
        По умолчанию строка считается кодом (flag = True).
        #################################################################
        In .asm file the method checks the line is code or not.
        By default the string is considered as a code (flag = True).
        """
        flag = True
        # Поиск в начале строки (либо после нескольких пробелов) символа ';'.
        # Searching the character ';' at the beginning of the line or after several spaces from beginning.
        if re.search(r'^\s*;.*$', string):
            flag = False
        # Поиск пустой строки. Такая строка считается комментарием (flag = False).
        # Searching empty line. The line is considered as a comment (flag = False).
        elif re.search(r'^\s*$', string):
            flag = False

        return flag


class CLOCCalculator:
    """
    Класс, содержащий набор функций, вычисляющих кол-во строк кода.
    #################################################################
    The class contains methods, which check the string is code or not.
    """

    def __init__(self):
        self.my_clc_checker = CodeLineChecker()

    def cloc_line_number(self):
        """
        Метод возвращает номер текущей строки кода.
        #################################################################
        Returns the current line number in our program.
        """
        return inspect.currentframe().f_back.f_lineno

    def cloc_check_path_exist(self, path):
        """
        Метод проверяет существование введённого пути.
        По умолчанию путь существует.
        ############################################################
        Method checks input path existence.
        By default the path exists.
        """
        flag = True
        try:
            os.listdir(path)
        except:
            flag = False
            print(self.cloc_line_number(), "Невозможно найти указанный путь")
        return flag

    def cloc_file_search(self,
                         path,
                         absolute_level,
                         excel_file,
                         row,
                         number):
        """
        Метод производит рекурсивный обход папки. Находит файлы и вложенные
        папки. Для каждого файла и папки вызывается метод fc_file_information()
        и возвращается список с результирующими данными.
        ############################################################
        Method performs recursive crawling of the folder. Method finds files and
        nested folders. For each file and each folder fc_file_information()
        is called. The function returns list with data.
        """
        file_counter = 0
        try:
            path_list = os.listdir(path)
            # Первый проход. Поиск файлов.
            # First pass. Searching files.
            for each_name in path_list:
                full_path = path + '\\' + each_name
                if os.path.isdir(full_path):
                    pass
                else:
                    # Работаем только с файлами с расширением.
                    # Working only with files, which have the extension.
                    if '.' in each_name:
                        # Работаем только с файлами, расширения которых входят в список.
                        # Working only with files, which extensions are in FILE_NAME_EXTENSION_LIST.
                        if each_name[each_name.rindex('.'):].upper() in FILE_NAME_EXTENSION_LIST:
                            try:
                                # Вычисление уровня вложенности.
                                # Calculating nesting level.
                                level = full_path.count('\\') - absolute_level
                                file_counter += 1
                                if level == 1:
                                    number += 1
                                    number1 = number
                                else:
                                    number1 = str(number) + '.' + str(file_counter)
                                # Получение списка данных для текущей папки.
                                # Getting data list for current folder.
                                temp = self.cloc_file_informaton(full_path, level, number1)
                                # Запись в файл excel.
                                # Writing to excel file.
                                excel_file.ref_data_to_excel(row, temp)
                                # Переход на следующую строку в файле excel.
                                # Going to the next row in excel file.
                                row += 1
                            except:
                                print(self.cloc_line_number(), each_name, "Ошибка при работе с этим файлом")
            # Второй проход. Поиск папок.
            # Second pass. Searching folders.
            for each_name in path_list:
                full_path = path + '\\' + each_name
                if os.path.isdir(full_path):
                    # Вычисление уровня вложенности.
                    # Calculating nesting level.
                    level = full_path.count('\\') - absolute_level
                    file_counter += 1
                    if level == 1:
                        # Счётчик первой цифры.
                        # Counter of first numeral in number.
                        number += 1
                        number1 = number
                    else:
                        number1 = str(number) + '.' + str(file_counter)
                    # Получение списка данных для текущей папки.
                    # Getting data list for current folder.
                    temp = self.cloc_file_informaton(full_path, level, number1)
                    # Запись в файл excel.
                    # Writing to excel file.
                    excel_file.ref_data_to_excel(row, temp)
                    # Рекурсивный обход папки.
                    # Recursive crawling of the folder.
                    row = self.cloc_file_search(full_path, absolute_level, excel_file, row + 1, number1)

        except:
            print(self.cloc_line_number(), path)
        return row

    def cloc_file_informaton(self,
                             full_path,
                             level,
                             number):
        """
        Получаем список данных для переданного файла/папки.
        ############################################################
        Getting list of data for transferred file/folder.
        """
        # Получение имени файла/папки.
        # Getting file/folder name.
        file_name = full_path[full_path.rindex('\\'):]
        file_name = file_name[1:]
        # Получение пути к файлу/папки.
        # Getting path of file/folder.
        folder_path = full_path[:full_path.rindex('\\')]
        local_list = []
        try:
            # Дата последнего изменения.
            # Last modified date.
            last_modified_time = time.strftime("%d.%m.%Y", time.gmtime(os.path.getmtime(full_path)))
            if os.path.isfile(full_path):
                # Получение расширения файла.
                # Getting file extension.
                file_extension = file_name[file_name.rindex('.'):]
                cloc = ''
                if file_extension.upper() in ['.CPP', '.C', '.H']:
                    cloc = self.cloc_calculate_c_cpp_h(full_path)
                elif file_extension.upper() in ['.ASM']:
                    cloc = self.cloc_calculate_asm(full_path)
                elif file_extension.upper() in ['.PY']:
                    cloc = self.cloc_calculate_py(full_path)
                # file_size = round(os.path.getsize(full_path) / 1024, 3)
                # Добавление данных в список.
                # Adding data to list.
                local_list = [folder_path, number, file_name, level, file_extension, cloc, '', last_modified_time]
            elif os.path.isdir(full_path):
                cloc = ''
                # file_size = self.cloc_folder_size(full_path)
                # Добавление данных в список.
                # Adding data to list.
                local_list = [folder_path, number, file_name, level, 'folder', cloc, '', last_modified_time]
        except:
            print(self.cloc_line_number(), file_name, "Ошибка при работе с этим файлом")
        return local_list

    def cloc_folder_size(self, path):
        """
        Вычисление размера папки (Кб).
        #################################################################
        Calculating size of folder (Kb).
        """
        folder_size = 0
        for each_file in os.listdir(path):
            full_path = path + '\\' + each_file
            if os.path.isfile(full_path):
                folder_size += round(os.path.getsize(full_path) / 1024, 3)
            elif os.path.isdir(full_path):
                folder_size += self.cloc_folder_size(full_path)
        return folder_size

    def cloc_text_to_dict(self, full_path):
        """
        Метод преобразует файл в словарь с ключами из номеров строк.
        Метод работает с кодировками, содержащимися в глобальной переменной
        ENCODINGS_LIST.
        #################################################################
        The method converts file into dictionary. Line numbers are keys.
        The method works file extensions only from global variable
        ENCODINGS_LIST.
        """
        i = 0
        dictionary = dict()
        flag = False
        for each in ENCODINGS_LIST:
            try:
                file_to_parse = open(os.path.abspath(full_path), 'r', encoding=each)
                for each_line in file_to_parse:
                    i += 1
                    dictionary[i] = each_line
                flag = True
                return dictionary
            except:
                pass
        if not flag:
            print(self.cloc_line_number(), '    неизвестная кодировка    ', full_path)

    def cloc_calculate_py(self, full_path):
        """
        # Метод вычисляет кол-во строк кода в файлах .py.
        ############################################################
        # The method calculates code lines count in .py.
        """
        dict_text_file = self.cloc_text_to_dict(full_path)
        count = 0
        i = 1
        while i <= len(dict_text_file):
            # Поиск однострочного блочного комментария вида """любой текст""".
            # Searching for a single-line comment like """any text""".
            if re.search(r'^\s*"""\s*\S*\s*\S*\s*\S*\s*\S*\s*\S*\s*\S*"""', dict_text_file[i]):
                i += 1
                continue
                # Поиск однострочного блочного комментария вида '''любой текст'''.
                # Searching for a single-line comment like '''any text'''.
            elif re.search(r'^\s*\'\'\'\s*\S*\s*\S*\s*\S*\s*\S*\s*\S*\s*\S*\'\'\'', dict_text_file[i]):
                i += 1
                continue
            # Поиск начала блочного комментария вида """.
            # Searching for the beginning of a block-type comment """.
            elif re.search(r'^"""', dict_text_file[i]):
                i += 1
                # Поиск конца блочного комментария вида """.
                # Searching for the end of a block-type comment """.
                while not bool(re.search(r'"""', dict_text_file[i])):
                    i += 1
                i += 1
                continue
            # Поиск начала блочного комментария вида '''.
            # Searching for the beginning of a block-type comment '''.
            elif re.search(r'^\'\'\'', dict_text_file[i]):
                i += 1
                # Поиск конца блочного комментария вида '''.
                # Searching for the end of a block-type comment '''.
                while not bool(re.search(r'\'\'\'', dict_text_file[i])):
                    i += 1
                i += 1
                continue

            # Проверка текущей строки кода.
            # Checking for current line of code.
            flag = self.my_clc_checker.clc_check_py(dict_text_file[i])
            if flag:
                count += 1
            i += 1
        dict_text_file.clear()
        return count

    def cloc_calculate_c_cpp_h(self, full_path):
        """
        # Метод вычисляет кол-во строк кода в файлах .c; .cpp; .h.
        ############################################################
        # The method calculates code lines count in .c; .cpp; .h.
        """
        dict_text_file = self.cloc_text_to_dict(full_path)
        count = 0
        i = 1
        while i <= len(dict_text_file):
            # Поиск однострочного блочного комментария вида /*любой текст*/.
            # Searching for a single-line comment like /*any text*/.
            if re.search(r'^/\*', dict_text_file[i]) and re.search(r'\*/', dict_text_file[i]):
                i += 1
                continue
            # Поиск начала блочного комментария вида /*.
            # Searching for the beginning of a block-type comment /*.
            elif re.search(r'^/\*', dict_text_file[i]):
                i += 1
                # Поиск конца блочного комментария вида */.
                # Searching for the end of a block-type comment */.
                while not bool(re.search(r'\*/', dict_text_file[i])):
                    i += 1
                i += 1
                continue

            # Проверка текущей строки кода.
            # Checking for current line of code.
            flag = self.my_clc_checker.clc_check_c_cpp_h(dict_text_file[i])
            if flag:
                count += 1
            i += 1
        dict_text_file.clear()
        return count

    def cloc_calculate_asm(self, full_path):
        """
        # Метод вычисляет кол-во строк кода в файлах .asm.
        ############################################################
        # The method calculates code lines count in .asm.
        """
        dict_text_file = self.cloc_text_to_dict(full_path)
        count = 0
        i = 1
        while i <= len(dict_text_file):
            # Проверка текущей строки кода.
            # Checking for current line of code.
            flag = self.my_clc_checker.clc_check_asm(dict_text_file[i])
            if flag:
                count += 1
            i += 1
        dict_text_file.clear()
        return count


class ResultExcelFile:
    """
    Класс, содержащий набор методов, работающих с файлом excel.
    ############################################################
    Class consists methods, which work with excel files.
    """

    def __init__(self):
        self.filename = self.ref_get_result_file_name()
        # Создание файла excel, куда будут записываться результаты
        # Creating excel file. The data will be add to this file
        self.workbook = xlsxwriter.Workbook(self.filename)
        # Создание листа в файле excel
        # Creating new sheet in excel file
        self.worksheet = self.ref_create_result_sheet()
        # Создание форматов ячеек для разных типов файлов (папка/файл)
        # Creating cell formats for different file types (folder/file)
        self.format_folder = self.ref_excel_cell_format_type(self.workbook, True, False, 'times new roman', 12)
        self.format_file = self.ref_excel_cell_format_type(self.workbook, False, False, 'times new roman', 10)

    def ref_get_result_file_name(self):
        """
        Создание нового файла result.xlsx, если такой уже существует.
        ############################################################
        The method creates new result.xlsx file, if it already exists.
        """
        if os.path.isfile('Results0.xlsx'):
            result_file_count = 1
            while os.path.isfile('Results' + str(result_file_count) + '.xlsx'):
                result_file_count += 1
            return 'Results' + str(result_file_count) + '.xlsx'
        else:
            return 'Results0.xlsx'

    def ref_create_result_sheet(self):
        """
        # Метод создаёт лист в файле excel, форматирует строки/столбцы и добавляет их название.
        ############################################################
        # The method creates sheet in excel file, formats rows/columns and adds their names.
        """
        worksheet = self.workbook.add_worksheet()
        format1 = self.ref_excel_cell_format_type(self.workbook, True, True, 'times new roman', 13)
        format2 = self.ref_excel_cell_format_type(self.workbook, True, False, 'times new roman', 13)

        worksheet.set_row(0, 10)
        worksheet.set_column(0, 1, 2)
        worksheet.set_column(2, 2, 4)
        worksheet.set_column(3, 13, 2)
        worksheet.set_column(14, 14, 40)
        worksheet.set_column(15, 15, 7)
        worksheet.set_column(16, 16, 7)
        worksheet.set_column(17, 17, 9)
        worksheet.set_column(18, 18, 13)

        worksheet.write(1, 1, 'Имя файла/папки', format2)
        worksheet.write(1, 15, 'Тип', format2)
        worksheet.write(1, 16, 'CLOC', format2)
        worksheet.write(1, 17, 'Размер, кБ', format1)
        worksheet.write(1, 18, 'Дата последнего изменения', format1)
        return worksheet

    def ref_create_sheet_heading(self, global_path):
        """
        Метод создаёт заголовок, записывает туда абсолютный путь.
        ############################################################
        The method creates heading and writes global path there.
        """
        format2 = self.ref_excel_cell_format_type(self.workbook, True, False, 'times new roman', 12)
        self.worksheet.write(3, 1, global_path, format2)

    def ref_excel_cell_format_type(self,
                                   workbook,
                                   bold,
                                   wrap,
                                   font,
                                   size):
        """
        Метод создаёт формат ячейки.
        ############################################################
        The method creates excel cell format.
        """
        format = workbook.add_format()
        format.set_bold(bold)
        format.set_text_wrap(wrap)
        format.set_font_name(font)
        format.set_font_size(size)
        format.set_align('left')
        format.set_align('vcenter')
        return format

    def ref_add_result_to_sheet(self,
                                row,
                                column,
                                data,
                                format):
        """
        Метод добавляет результаты в конкретную ячейку
        листа worksheet. Форматирование - format.
        ############################################################
        The method adds results to a specific cell in excel worksheet.
        Format - format.
        """
        self.worksheet.write(row, column, data, format)

    def ref_data_to_excel(self,
                          row,
                          list):
        """
        Метод записывает данные в файл excel.
        ############################################################
        The method adds results to excel file.
        """
        format_file = self.format_file
        format_folder = self.format_folder

        if list[4]=='folder':
            current_format = format_folder
            self.ref_add_result_to_sheet(row, 2, list[1], current_format)
            self.ref_add_result_to_sheet(row, list[3] + 2, list[2], current_format)
            self.ref_add_result_to_sheet(row, 15, list[4], current_format)
            self.ref_add_result_to_sheet(row, 16, list[5], current_format)
        else:
            current_format = format_file
            self.ref_add_result_to_sheet(row, 2, list[1], current_format)
            self.ref_add_result_to_sheet(row, list[3] + 2, list[2], current_format)
            self.ref_add_result_to_sheet(row, 15, list[4], current_format)
            self.ref_add_result_to_sheet(row, 16, list[5], current_format)

        self.ref_add_result_to_sheet(row, 17, list[6], format_file)
        self.ref_add_result_to_sheet(row, 18, list[7], format_file)


# Ввод адреса, создание файла, листа, форматов, получение результатов
def main(target_folder):
    time_start = int(round(time.time() * 1000))
    # Экземляр класса, считающего строки кода
    my_cloc_calculator = CLOCCalculator()
    flag = my_cloc_calculator.cloc_check_path_exist(target_folder)
    if flag:
        absolute_level = target_folder.count('\\')
        my_excel_file = ResultExcelFile()
        my_excel_file.ref_create_sheet_heading(target_folder)
        my_cloc_calculator.cloc_file_search(target_folder, absolute_level, my_excel_file, 4, 0)
        my_excel_file.workbook.close()

    time_finish = int(round(time.time() * 1000))
    print(time_finish - time_start, 'ms')


# Ввод пути к папке, в которой будет производиться поиск файлов
target_folder_path = r'PUT FOLDER PATH HERE'
main(target_folder_path)
