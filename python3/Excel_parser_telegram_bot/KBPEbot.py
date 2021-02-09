# coding: utf-8

"""
Telegram-bot, который по запросу выдает список тех задач, которые были
выполнены за сегодня.
##############################################################################
The telegram-bot which outputs list of performed tasks by request.
"""

import telepot
import openpyxl
from maincode import maincode
from constants import token
from constants import folder_path

class TelegramBot(telepot.Bot):
    '''
    Класс, описывающий телеграм-бота и содержащий методы для вывода нужной
    информации.
    ##########################################################################
    The class describes telegram-bot and contains methods to output needed
    data.
    '''

    def __init__(self, token):
        telepot.Bot.__init__(self, token)

    def main(self, message):
        '''
        Главный метод. Вызывает другие методы по запросу.
        ######################################################################
        The main method which calls other methods by request.
        '''

        content_type, chat_type, chat_id = telepot.glance(message)
        if content_type == 'text':
            # Команда /result.
            # /result command.
            if message['text'] == '/result':
                self.result_types(chat_id, 'Выберите лист:')

            # Команда /sheet1. Вывод выполненных задач по листу 1.
            ##################################################################
            # /sheet1 command. Outputting performed tasks for sheet 1.
            elif message['text'] in self.sheet_dict():
                try:
                    sheet_index = self.sheet_dict()[message['text']]
                    # Получение словаря, где ключи - номера выполненных
                    # за сегодня задач, значения - описания задач.
                    ##########################################################
                    # Getting dictionary, where number of performed tasks
                    # are KEYS, and tasks description are VALUES.
                    dict = maincode(folder_path, sheet_index)
                    # Вывод задач.
                    ##########################################################
                    # Output data.
                    self.show_tasks(chat_id, dict)
                except:
                    # Вывод сообщения об ошибке и списка команд для
                    # продолжения работы.
                    ##########################################################
                    # Outputting error message and list of commands to
                    # continue work with bot.
                    text = 'Возникла ошибка при обработке excel файла.\n' \
                           'Обратитесь к разработчику. \n Выберите лист:'
                    self.result_types(chat_id, text)

            # Любой текст.
            ##################################################################
            # Any text.
            else:
                self.start(chat_id)

    def start(self, chat_id):
        '''
        Метод, который вызывается при запуске бота, либо
        при неизвестной команде.
        ######################################################################
        The method which is called after bot start or
        when input any text.
        '''

        self.sendMessage(chat_id,
            '''
Приветствую. Я бот компании "КБ Проминжиниринг".
Моей основной задачей является анализ таблицы заданий,
поиск и вывод тех заданий, которые были выполнены за сегодня.
/result - получить список выполненных задач
            ''')

    def result_types(self, chat_id, text):
        '''
        Метод, который выводит перечель листов файла excel, для которых можно
        выполнить вывод выполненных задач.
        ######################################################################
        The method outputs list of excel file`s sheets. The bot would work
        only with this sheets.
        '''

        today_full_path = folder_path + r'/New.xlsx'
        today_wb = openpyxl.load_workbook(today_full_path)
        # Получение списка всех листов в этой книге.
        ######################################################################
        # Getting list of sheets in this book.
        sheets_names = today_wb.get_sheet_names()
        message = text + '\n'
        i = 0
        # Формирование списка команд.
        ######################################################################
        # Forming list of commands.
        while i<9:
            message += '/sheet' + str(i+1) + ' - лист "' + sheets_names[i]\
                       + '"' + '\n'
            i += 1
        message += '/start - вернуться в начало'
        self.sendMessage(chat_id, message)

    def sheet_dict(self):
        '''
        Метод, который формирует словарь, где ключи - команды, значения -
        номера листов.
        ######################################################################
        The method returns dictionary, where commands are KEYS, sheets numbers
        are VALUES.
        '''

        command_dict = {}
        i = 0
        while i < 9:
            command_dict['/sheet' + str(i+1)] = i
            i += 1
        return command_dict

    def show_tasks(self, chat_id, tasks_dictionary):
        '''
        Метод, который выводит список выполненных задач. Задачи берутся из
        tasks_dictionary. В конце выводится список команд для бота.
        ######################################################################
        The method outputs list of performed tasks. The tasks are taken from
        tasks_dictionary. The list of bot`s commands is output at the end.
        '''

        # Случай, когда словарь выполненных задач пуст.
        ######################################################################
        # The case when the tasks_dictionary is empty.
        if len(tasks_dictionary) == 0:
            self.sendMessage(chat_id, 'За сегодня не выполнено ни одного задания.')
            # Случай, когда словарь выполненных задач НЕ пуст.
            ##################################################################
            # The case when the tasks_dictionary is NOT empty.
        else:
            self.sendMessage(chat_id, 'За сегодня выполнены задания:')
            i = 1
            for each in tasks_dictionary:
                answer = str(i) + ") Задание № " + str(each) + ': ' + str(tasks_dictionary[each])
                self.sendMessage(chat_id, answer)
                i += 1
        self.result_types(chat_id, 'Выберите лист:')

# Создание экземпляра класса.
# Creating an instance of the class.
KBPEbot = TelegramBot(token)
# Запуск бота навсегда (до принудительной остановки).
# Run the bot forever (before the forced stop).
KBPEbot.message_loop({'chat':KBPEbot.main}, run_forever=True)
