# coding cp1251

import xlsxwriter
import os
import pymysql
MYSQL_CONNECT = ["host", "name", "password", "schema"]

connection = pymysql.connect(MYSQL_CONNECT[0],
                             MYSQL_CONNECT[1],
                             MYSQL_CONNECT[2],
                             MYSQL_CONNECT[3],
                             charset='cp1251')


class ResultExcelFile:
    """
    Класс, содержащий набор методов, работающих с файлом excel.
    ##########################################################################
    Class consists methods, which work with excel files.
    """

    def __init__(self):
        """
        Генерирование имени файла excel.
        Создание файла excel.
        Создание листа в этом файле.
        Создание форматов ячеек.
        ######################################################################
        Generating the excel file name .
        Creating excel file. The data will be add to this file.
        Creating new sheet in excel file.
        Creating cell formats.
        """

        self.filename = self.__ref_get_result_file_name()
        self.workbook = xlsxwriter.Workbook(self.filename)
        self.worksheet = self.__ref_create_result_sheet()
        self.format_header1 = self.ref_excel_cell_format_type(
            self.workbook, True, False,
            'times new roman', 14, 'left', 'vcenter')
        self.format_header2 = self.ref_excel_cell_format_type(
            self.workbook, True, False,
            'times new roman', 13, 'left', 'vcenter')
        self.format_header3 = self.ref_excel_cell_format_type(
            self.workbook, True, True,
            'times new roman', 12,  'center', 'vcenter')
        self.format_text = self.ref_excel_cell_format_type(
            self.workbook, False, False,
            'times new roman', 10,  'left', 'vcenter')

    def __ref_get_result_file_name(self):
        """
        Создание нового файла result.xlsx, если такой уже существует.
        ######################################################################
        The method creates new result.xlsx file, if it already exists.
        """

        if os.path.isfile('Results0.xlsx'):
            result_file_count = 1
            while os.path.isfile('Results' + str(result_file_count) + '.xlsx'):
                result_file_count += 1
            return 'Results' + str(result_file_count) + '.xlsx'
        else:
            return 'Results0.xlsx'

    def __ref_create_result_sheet(self):
        """
        Функция создаёт лист в файле excel, форматирует строки/столбцы.
        ######################################################################
        The function creates sheet in excel file, formats rows/columns.
        """

        worksheet = self.workbook.add_worksheet()
        worksheet.set_column(0, 0, 2)
        worksheet.set_column(1, 1, 3)
        worksheet.set_column(2, 2, 12)
        worksheet.set_column(3, 3, 15)
        worksheet.set_column(4, 4, 20)
        worksheet.set_column(5, 5, 25)
        worksheet.set_column(6, 6, 5)
        worksheet.set_column(7, 7, 18)
        worksheet.set_column(8, 8, 12)
        return worksheet

    def ref_create_header_string(self, row):
        """
        Функция создаёт строку с наименованиями.
        ######################################################################
        The function creates string with columns names.
        """

        self.worksheet.write(row, 1, '№', self.format_header3)
        self.worksheet.write(row, 2, 'Инв. №', self.format_header3)
        self.worksheet.write(row, 3, 'Идентиф. № / Заводской №',
                             self.format_header3)
        self.worksheet.write(row, 4, 'Наименование', self.format_header3)
        self.worksheet.write(row, 5, 'Марка', self.format_header3)
        self.worksheet.write(row, 6, 'Кол-во', self.format_header3)
        self.worksheet.write(row, 7, 'Предназначение', self.format_header3)
        self.worksheet.write(row, 8, 'Дата прибытия', self.format_header3)

    def ref_add_data_string(self, row, data):
        """
        Функция добавляет строку с данными.
        ######################################################################
        The function adds string with data.
        """

        self.worksheet.write(row, 1, data[1], self.format_text)
        self.worksheet.write(row, 2, data[2], self.format_text)
        self.worksheet.write(row, 3, data[3], self.format_text)
        self.worksheet.write(row, 4, data[4], self.format_text)
        self.worksheet.write(row, 5, data[5], self.format_text)
        self.worksheet.write(row, 6, data[6], self.format_text)
        self.worksheet.write(row, 7, data[7], self.format_text)
        date = ('%s.%s.%s') % (data[8].year, data[8].month, data[8].day)
        self.worksheet.write(row, 8, date, self.format_text)

    def ref_excel_cell_format_type(self, workbook,
                                   bold, wrap, font,
                                   size, horiz, vertic):
        """
        Метод создаёт формат ячейки.
        ######################################################################
        The method creates excel cell format.
        """

        format = workbook.add_format()
        format.set_bold(bold)
        format.set_text_wrap(wrap)
        format.set_font_name(font)
        format.set_font_size(size)
        format.set_align(horiz)
        format.set_align(vertic)
        return format


def get_all_project():
    query = 'CALL `get_all_proj`()'
    cursor = connection.cursor()
    cursor.execute(query)
    list = []
    for each in cursor._rows:
        list.append(each[0])
    return list


def get_all_detail_types():
    query = 'CALL `get_all_types`()'
    cursor = connection.cursor()
    cursor.execute(query)
    list = []
    for each in cursor._rows:
        list.append(each[0])
    return list


def get_all_id_by_proj(object):
    types_list = get_all_detail_types()
    obj_list = get_all_project()
    if (object in obj_list):
        local_dict = {}
        for detail_type in types_list:
            cursor = connection.cursor()
            query = 'CALL `get_all_id_by_type_proj`(\'%s\', \'%s\')' % (object, detail_type)
            try:
                cursor.execute(query)
            except:
                pass

            local_list = []
            for each1 in cursor._rows:
                local_list.append(each1[0])

            if len(local_list) != 0:
                local_dict[detail_type] = local_list

        return local_dict
    else:
        return {}


def get_all_id():
    obj_list = get_all_project()
    local_dict1 = {}
    for object in obj_list:
        try:
            local_dict = get_all_id_by_proj(object)
        except:
            local_dict = {}
        local_dict1[object] = local_dict

    return local_dict1


def get_all_info_by_id(id):
    cursor = connection.cursor()
    query = 'CALL `get_all_data_by_id`(\'%s\')' % id
    try:
        cursor.execute(query)
    except:
        pass

    return cursor._rows[0]


def print_all_data_to_excel():
    """
    Функция, которая выгружает данные по всем объектам
    из БД в файл excel.
    ##########################################################################
    The function prints data for all objects to excel file.
    """

    try:
        my_excel = ResultExcelFile()
        row = 1
        dictionary = get_all_id()
        for each_obj in dictionary:
            if len(dictionary[each_obj]) != 0:
                my_excel.worksheet.write(row, 1, each_obj,
                                         my_excel.format_header1)
                row += 1
                details_id_list = dictionary[each_obj]
                for each_detail in details_id_list:
                    my_excel.worksheet.write(row, 1, each_detail,
                                             my_excel.format_header2)
                    row += 1
                    my_excel.ref_create_header_string(row)
                    row += 1
                    for each_id in details_id_list[each_detail]:
                        try:
                            data = get_all_info_by_id(each_id)
                            print(data)
                            my_excel.ref_add_data_string(row, data)
                            row += 1
                        except:
                            pass
                    row += 2
            else:
                my_excel.worksheet.write(row, 1, each_obj +
                                         ' - детали отсутствуют.',
                                         my_excel.format_header1)
                row += 2
        my_excel.workbook.close()
    except:
        pass


def print_one_object_data_to_excel(object):
    """
    Функция, которая выгружает данные по одному объекту
    из БД в файл excel.
    ##########################################################################
    The function prints data for one object to excel file.
    """

    try:
        my_excel = ResultExcelFile()
        row = 1
        dictionary = get_all_id_by_proj(object)
        if len(dictionary) != 0:
            my_excel.worksheet.write(row, 1, object, my_excel.format_header1)
            row += 1
            for each_detail in dictionary:
                my_excel.worksheet.write(row, 1, each_detail,
                                         my_excel.format_header2)
                row += 1
                my_excel.ref_create_header_string(row)
                row += 1
                for each_id in dictionary[each_detail]:
                    try:
                        data = get_all_info_by_id(each_id)
                        my_excel.ref_add_data_string(row, data)
                        row += 1
                    except:
                        pass
                row += 2
        else:
            my_excel.worksheet.write(row, 1, object +
                                     ' - детали отсутствуют.',
                                     my_excel.format_header1)
            row += 2
        my_excel.workbook.close()
    except:
        pass


# print_all_data_to_excel()
# print_one_object_data_to_excel('БОП-04У(-01)')
# print_one_object_data_to_excel('СМ1820МВУ (Сервер)')
