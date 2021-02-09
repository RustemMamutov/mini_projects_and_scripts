# encoding: utf-8
"""
Программа предназначена для построения структуры файлов в заданной папке.
Программа определяет уровень вложенности, в соответствии с этим проставляет
номер (например, 4.6.1.2), также вычисляет размер файлов и папок.
Результат записывается в файл excel (.xlsx).
#################################################################
The program is designed to build files structure in the specified folder.
It determines level of nesting, indicates number (for example 4.6.1.2), and
also calculates files and folders size.
Results output to excel file (.xlsx).
"""

import os
import time
import xlsxwriter
import inspect

# Словарь расширений.
# Extension dictionary.
FILE_NAME_EXTENSION_DICT = {'.DOC':'Документ Word', '.DOCX':'Документ Word', '.XLS':'Документ Excel', '.XLSX':'Документ Excel',
                            '.PDF': 'Adobe Acrobat Reader', '.PPTX': 'Power Point'}


class FilesCalculator:
    """
    Класс, содержащий набор методов, вычисляющих кол-во строк кода в файле
    #################################################################
    The class contains methods, which calculate source lines of code
    in current file
    """

    def __init__(self):
        pass

    def fc_line_number(self):
        """
        Метод возвращает номер текущей строки кода.
        #################################################################
        Returns the current line number in our program.
        """
        return inspect.currentframe().f_back.f_lineno

    def fc_check_path_exist(self, path):
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
            print(self.fc_line_number(), "Невозможно найти указанный путь")
        return flag

    def fc_file_search(self, path, global_list, absolute_level, excel_file, row, number):
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
                    temp = self.fc_file_informaton(full_path, level, number1)
                    # Запись в файл excel.
                    # Writing to excel file.
                    excel_file.ref_data_to_excel(row, temp)
                    # Рекурсивный обход папки.
                    # Recursive crawling of the folder.
                    row = self.fc_file_search(full_path, global_list, absolute_level, excel_file, row + 1, number1)
            # Второй проход. Поиск папок.
            # Second pass. Searching files.
            for each_name in path_list:
                full_path = path + '\\' + each_name
                if os.path.isdir(full_path):
                    pass
                else:
                    try:
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
                        temp = self.fc_file_informaton(full_path, level, number1)
                        # Запись в файл excel.
                        # Writing to excel file.
                        excel_file.ref_data_to_excel(row, temp)
                        # Переход на следующую строку в файле excel.
                        # Going to the next row in excel file.
                        row += 1
                    except:
                        print(self.fc_line_number(), each_name, "Ошибка при работе с этим файлом")
        except:
            print(self.fc_line_number(), path)
        return row

    def fc_file_informaton(self, full_path, level, number):
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
                if '.' in file_name:
                    file_extension = file_name[file_name.rindex('.'):]
                else:
                    file_extension = 'none'
                # Замена расширения файла на название программы.
                # Replacement file extension to program name.
                if (file_extension.upper() in FILE_NAME_EXTENSION_DICT.keys()):
                    file_extension = FILE_NAME_EXTENSION_DICT[file_extension.upper()]
                # Вычисление размера файла.
                # Calculating file size.
                file_size = round(os.path.getsize(full_path) / 1024, 3)
                # Добавление данных в список.
                # Adding data to list.
                local_list = [folder_path, number, file_name, level, file_extension, file_size, last_modified_time]
            elif os.path.isdir(full_path):
                # Вычисление размера папки.
                # Calculating folder size.
                file_size = self.fc_folder_size(full_path)
                # Добавление данных в список.
                # Adding data to list.
                local_list = [folder_path, number, file_name, level, 'folder', file_size, last_modified_time]
        except:
            print(self.fc_line_number(), file_name, "Ошибка при работе с этим файлом")
        return local_list

    def fc_folder_size(self, path):
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
                folder_size += self.fc_folder_size(full_path)
        return folder_size


class ResultExcelFile:
    """
    Класс, содержащий набор методов, работающих с файлом excel.
    ############################################################
    Class consists methods, which work with excel files.
    """

    def __init__(self):
        """
        Генерирование имени файла excel.
        Создание файла excel.
        Создание листа в этом файле.
        Создание форматов ячеек для разных типов файлов (папка/файл).
        ############################################################
        Generating the excel file name .
        Creating excel file. The data will be add to this file.
        Creating new sheet in excel file.
        Creating cell formats for different file types (folder/file).
        """
        self.filename = self.ref_get_result_file_name()
        self.workbook = xlsxwriter.Workbook(self.filename)
        self.worksheet = self.ref_create_result_sheet()
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
        Функция создаёт лист в файле excel, форматирует строки/столбцы и добавляет их название.
        ############################################################
        The function creates sheet in excel file, formats rows/columns and adds their names.
        """
        worksheet = self.workbook.add_worksheet()
        format1 = self.ref_excel_cell_format_type(self.workbook, True, True, 'times new roman', 13)
        format2 = self.ref_excel_cell_format_type(self.workbook, True, False, 'times new roman', 13)

        worksheet.set_row(0, 10)
        worksheet.set_column(0, 1, 2)
        worksheet.set_column(2, 2, 4)
        worksheet.set_column(3, 13, 2)
        worksheet.set_column(14, 14, 30)
        worksheet.set_column(15, 15, 20)
        worksheet.set_column(16, 16, 15)
        worksheet.set_column(17, 17, 15)

        worksheet.write(1, 1, 'Имя файла/папки', format2)
        worksheet.write(1, 15, 'Тип', format2)
        worksheet.write(1, 16, 'Размер, кБ', format1)
        worksheet.write(1, 17, 'Дата последнего изменения', format1)
        return worksheet

    def ref_create_sheet_heading(self, global_path):
        """
        Метод создает заголовок.
        ############################################################
        The method creates heading.
        """
        format2 = self.ref_excel_cell_format_type(self.workbook, True, False, 'times new roman', 12)
        self.worksheet.write(3, 1, global_path, format2)

    def ref_excel_cell_format_type(self, workbook, bold, wrap, font, size):
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

    def ref_add_result_to_sheet(self, row, column, data, format):
        """
        Метод добавляет результаты в конкретную ячейку листа worksheet.
        Форматирование - format
        ############################################################
        The method adds results in specific cell in worksheet.
        Format - format
        """
        self.worksheet.write(row, column, data, format)

    def ref_data_to_excel(self, row, list):
        """
        Метод записывает данные в файл excel.
        ############################################################
        The method adds data to excel file.
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


def main(target_folder):
    """
    Ввод адреса, создание файла, получение результатов
    ############################################################
    Inputting path, creating file, getting results
    """
    # Время начала выполнения
    # Start time
    time_start = int(round(time.time() * 1000))
    # Экземляр класса для получения структуры файлов
    # Instance of class to get files structure
    my_fc_calculator = FilesCalculator()
    # Проверка существования введенного пути
    # Checking input path existence
    flag = my_fc_calculator.fc_check_path_exist(target_folder)
    if flag:
        # Вычисление уровня вложенности введённой папки
        # Calculating nesting level for current folder
        absolute_level = target_folder.count('\\')
        # Экземляр класса для работы с excel файлами
        # Instance of class to work with excel files
        my_excel_file = ResultExcelFile()
        # Создание заголовка в файле
        # Creating heading in file
        my_excel_file.ref_create_sheet_heading(target_folder)
        # Создание структуры файлов
        # Creating files structure
        my_fc_calculator.fc_file_search(target_folder, [], absolute_level, my_excel_file, 4, 0)
        # Закрытие книги excel
        # Excel workbook closing
        my_excel_file.workbook.close()

    # Время конца выполнения
    # Finish time
    time_finish = int(round(time.time() * 1000))
    # Время работы программы
    # Program work time
    print(time_finish-time_start, 'ms')


# Entering the path of folder, where files structure should be get
target_folder_path = r'PUT FOLDER PATH HERE'
main(target_folder_path)
