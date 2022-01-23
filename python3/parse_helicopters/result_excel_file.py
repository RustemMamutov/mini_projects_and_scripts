import xlsxwriter
import os


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
            'times new roman', 12, 'left', 'vcenter')
        self.format_text = self.ref_excel_cell_format_type(
            self.workbook, False, False,
            'times new roman', 12,  'left', 'vcenter')

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
        The function creates sheet in excel file, formats rows/columns.
        """

        worksheet = self.workbook.add_worksheet()
        worksheet.set_column(0, 0, 2)
        worksheet.set_column(1, 1, 5)
        worksheet.set_column(2, 2, 10)
        worksheet.set_column(3, 3, 30)
        worksheet.set_column(4, 4, 20)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 10)
        worksheet.set_column(8, 8, 10)
        worksheet.set_column(9, 9, 10)
        return worksheet

    def ref_create_header_string(self, row, data):
        """
        The function creates string with columns names.
        """
        for i in range(0, len(data)):
            self.worksheet.write(row, i+1, data[i], self.format_header1)

    def ref_add_data_to_cell(self, row, cell, text):
        """
        The function adds string with data.
        """
        self.worksheet.write(row, cell, text, self.format_text)

    def ref_add_data_string(self, row, hell_info):
        """
        The function adds string with data.
        """
        self.worksheet.write(row, 1, hell_info.num, self.format_text)
        self.worksheet.write(row, 2, hell_info.id, self.format_text)
        self.worksheet.write(row, 3, hell_info.name, self.format_text)
        self.worksheet.write(row, 4, hell_info.price, self.format_text)
        self.worksheet.write(row, 5, hell_info.year, self.format_text)
        self.worksheet.write(row, 6, hell_info.serial_num, self.format_text)
        self.worksheet.write(row, 7, hell_info.ttaf, self.format_text)
        self.worksheet.write(row, 8, hell_info.location, self.format_text)
        self.worksheet.write(row, 9, hell_info.info, self.format_text)
        self.worksheet.write(row, 10, hell_info.link, self.format_text)

    def ref_excel_cell_format_type(self, workbook, bold, wrap, font, size, horiz, vertic):
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