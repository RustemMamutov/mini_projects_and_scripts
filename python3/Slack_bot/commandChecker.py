import datetime
import MySQLdb

# Список с данными для подключения к БД MySql: ip сервера, логин, пароль,
# название БД.
##############################################################################
# List of data to connect MySql database: server ip, login, password, db name.
from constants import MYSQL_CONNECT

class commandChecker():
    '''
    Класс, который проверяет правильность команд.
    ##########################################################################
    The class checks correctness of the commands.
    '''

    def __init__(self):
        self.flag = True
        self.answer = ''
        self.connection = MySQLdb.connect(MYSQL_CONNECT[0],
                                          MYSQL_CONNECT[1],
                                          MYSQL_CONNECT[2],
                                          MYSQL_CONNECT[3])


    def make_employees_list(self):
        '''
        Метод составляет список сотрудников из таблицы KBPE.Users.
        ######################################################################
        The method makes list of employees from KBPE.Users table.
        '''

        mysql_query = 'select*from KBPE.Users;'
        local_parser = commandChecker()
        cursor = local_parser.connection.cursor()
        cursor.execute(mysql_query)
        employees_list = []
        for each in cursor._rows:
            employees_list.append(each[1].lower())
        return employees_list


    def make_locations_list(self):
        '''
        Метод составляет список мест работы из таблицы KBPE.Locations.
        ######################################################################
        The method makes list of work places from KBPE.Locations table.
        '''

        mysql_query = 'select*from KBPE.Locations;'
        local_parser = commandChecker()
        cursor = local_parser.connection.cursor()
        cursor.execute(mysql_query)
        locations_list = []
        for each in cursor._rows:
            locations_list.append(each[1].lower())
        return locations_list


    def cc_check_name(self, flag, answer, text):
        '''
        Метод проверяет имя. Имя должно входить в список names.
        ######################################################################
        The method checks name. The name must be in list of names.
        '''

        employees = self.make_employees_list()
        if text.lower() in employees:
            pass
        else:
            flag = False
            answer += 'Ошибка в имени. '
        return answer, flag


    def cc_check_date(self, flag, answer, text):
        '''
        Метод проверяет дату.
        ######################################################################
        The method checks date.
        '''

        date = ''
        try:
            if datetime.datetime.strptime(text, '%Y.%m.%d'):
                list = text.split('.')
                # Формирование даты в виде гггг.мм.дд.
                ##############################################################
                # Forming date in format yyyy.mm.dd.
                if len(list[1]) == 1:
                    list[1] = '0' + list[1]
                if len(list[2]) == 1:
                    list[2] = '0' + list[2]
                date = list[0] + '.' + list[1] + '.' + list[2]
        except:
            flag = False
            answer += 'Ошибка в дате. '
        return answer, flag, date


    def check_location(self, flag, answer, text):
        '''
        Метод проверяет место работы.
        Место должно входить в список locations.
        ######################################################################
        The method checks location.
        The location must be in list of locations.
        '''

        locations = self.make_locations_list()
        if text.lower() in locations:
            pass
        else:
            flag = False
            answer += 'Ошибка в месте работы. '
        return answer, flag


    def cc_set_day_input_check(self, text):
        '''
        Метод проверяет всю команду целиком.
        ######################################################################
        The method checks the entire command.
        '''

        def check_time(flag, answer, text):
            '''
            Метод проверяет время.
            ##################################################################
            The method checks time.
            '''

            time = ''
            try:
                try:
                    if datetime.datetime.strptime(text, "%H.%M"):
                        list = text.split('.')
                        # Формирование времени в виде ЧЧ:ММ.
                        ######################################################
                        #  Forming time in format HH:MM.
                        if len(list[0]) == 1:
                            list[0] = '0' + list[0]
                        time = list[0] + ':' + list[1]
                except:
                    try:
                        if datetime.datetime.strptime(text, "%H:%M"):
                            list = text.split(':')
                            # Формирование времени в виде ЧЧ:ММ.
                            ##################################################
                            #  Forming time in format HH:MM.
                            if len(list[0]) == 1:
                                list[0] = '0' + list[0]
                            time = list[0] + ':' + list[1]
                    except:
                        flag = False
                        answer += 'Ошибка во времени. '
            except:
                flag = False
                answer += 'Ошибка во времени. '
            return answer, flag, time

        def check_time_period(flag, answer, text1, text2):
            '''
            Метод проверяет временной период.
            Время начала рабочего дня не может быть больше времени окончания
            рабочего дня.
            ##################################################################
            The method checks time period.
            The work day start time can`t be more than finish time.
            '''

            if (text1 < text2):
                pass
            else:
                flag = False
                answer += 'Ошибка во времени - начало позже конца. '
            return answer, flag

        answer = ''
        flag = True
        if type(text) is list:
            local_list = text
        else:
            local_list = text.split(' ')

        # Проверка длины введённой команды. Может быть либо 4, либо 5 слов.
        ######################################################################
        # Checking of command length. There can be only 4 or 5 words.
        if (len(local_list) == 5 or len(local_list) == 4):
            pass
        elif len(local_list) == 3:
            local_list.append('+')
        else:
            flag = False
            answer += 'Неполная или избыточная команда. '

        # Проверка имени.
        ######################################################################
        # Checking of name.
        if flag:
            answer, flag = self.cc_check_name(flag, answer, local_list[0])

        # Проверка места работы.
        ######################################################################
        # Checking of location.
        if flag:
            answer, flag = self.check_location(flag, answer, local_list[1])

        # Проверка даты.
        ######################################################################
        # Checking of date.
        if flag:
            answer, flag, date = self.cc_check_date(flag, answer,
                                                    local_list[2])
            local_list[2] = date

        # Проверка времени.
        ######################################################################
        # Checking of time.
        if flag:
            if (len(local_list) == 4):
                if local_list[3] == '+':
                    local_list[3] = '10:00'
                    local_list.append('19:00')
                else:
                    flag = False
                    answer += 'Некорректная команда. '
            else:
                if flag:
                    answer, flag, time = check_time(flag, answer,
                                                    local_list[3])
                    local_list[3] = time
                if flag:
                    if (local_list[4]) == '+':
                        local_list[4] = '19:00'
                    else:
                        answer, flag, time = check_time(flag, answer,
                                                        local_list[4])
                        local_list[4] = time
                        if flag:
                            answer, flag = check_time_period(flag, answer,
                                                             local_list[3],
                                                             local_list[4])

        return flag, answer, local_list


    def cc_get_day_input_check(self, text):
        '''
        Метод проверяет всю команду целиком.
        ######################################################################
        The method checks the entire command.
        '''

        answer = ''
        flag = True
        list = text.split(' ')

        # Проверка длины введённой команды. Может быть только 2 слова.
        ######################################################################
        # Checking of command length. There can be only 2 words.
        if (len(list) == 2):
            pass
        else:
            flag = False
            answer += 'Неполная или избыточная команда. '

        # Проверка имени.
        ######################################################################
        # Checking of name.
        if flag:
            answer, flag = self.cc_check_name(flag, answer, list[0])

        # Проверка даты.
        ######################################################################
        # Checking of date.
        if flag:
            answer, flag, date = self.cc_check_date(flag, answer, list[1])
            list[1] = date

        return flag, answer, list


    def cc_get_week_input_check(self, text):
        '''
        Метод проверяет всю команду целиком.
        ######################################################################
        The method checks the entire command.
        '''

        answer = ''
        flag = True
        list = text.split(' ')

        # Проверка длины введённой команды. Может быть только 1 слово.
        ######################################################################
        # Checking of command length. There can be only 1 word.
        if (len(list) == 1):
            pass
        else:
            flag = False
            answer += 'Неполная или избыточная команда. '

        # Проверка имени.
        ######################################################################
        # Checking of name.
        if flag:
            answer, flag = self.cc_check_name(flag, answer, text)

        return flag, answer, text
