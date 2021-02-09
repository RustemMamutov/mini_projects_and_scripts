import MySQLdb
import calendar
from commandChecker import commandChecker
from calendarSearcher import calendarSearcher

# Список с данными для подключения к БД MySql: ip сервера, логин, пароль,
# название БД.
##############################################################################
# List of data to connect MySql database: server ip, login, password, db name.
from constants import MYSQL_CONNECT
from constants import WEEKDAYS
from constants import HOLIDAYS


class mysqlScheduleParser():
    '''
    Класс работает с БД MySql, может добавлять и получать данные из БД.
    ##########################################################################
    The class works with MySql DB, it can write to DB, and read from DB.
    '''

    def __init__(self):
        self.checker = commandChecker()
        self.my_searcher = calendarSearcher()
        self.connection = MySQLdb.connect(MYSQL_CONNECT[0],
                                          MYSQL_CONNECT[1],
                                          MYSQL_CONNECT[2],
                                          MYSQL_CONNECT[3])


    def msp_add_employee(self, name):
        '''
        Метод добавляет сотрудника в таблицу KBPE.Users.
        ######################################################################
        The method adds employee to KBPE.Users table.
        '''

        def make_query(text):
            '''
            Метод формирует запрос на языке SQL, который добавит сотрудника
            в таблицу KBPE.Users.
            ##################################################################
            The method generates a SQL query, which adds employee
            to KBPE.Users table.
            '''

            # Формирование запроса для проверки наличия сотрудника с таким
            # именем в таблице KBPE.Users.
            ##################################################################
            # Generating sql-query for checking existence of the employee
            # in KBPE.Users table.
            local_query_form =\
                'select*from KBPE.Users where user_name = \'%s\';'
            local_query = local_query_form % (text)

            local_parser = mysqlScheduleParser()
            cursor = local_parser.connection.cursor()
            count = cursor.execute(local_query)
            if count == 0:
                flag = True
            else:
                flag = False

            # Формирование итогового sql-запроса.
            ##################################################################
            # Generating final sql-query.
            if flag:
                mysql_query_form =\
                    'Replace KBPE.Users (user_name) VALUES (\'%s\');'
                mysql_query = mysql_query_form % (text)
            else:
                mysql_query = ''
            return flag, mysql_query

        flag, mysql_query = make_query(name)
        if flag:
            try:
                local_parser = mysqlScheduleParser()
                cursor = local_parser.connection.cursor()
                cursor.execute(mysql_query)
                local_parser.connection.commit()
                local_parser.connection.close()
                return 'Новый сотрудник добавлен.'
            except:
                return 'Ошибка в добавлении сотрудника.'
        else:
            return 'Такой сотрудник уже есть в БД.'


    def msp_add_location(self, location):
        '''
        Метод добавляет место работы в таблицу KBPE.Locations.
        ######################################################################
        The method adds work location to KBPE.Locations table.
        '''

        def make_query(text):
            '''
            Метод формирует запрос на языке SQL, который добавит место работы
            в таблицу KBPE.Locations.
            ##################################################################
            The method generates a SQL query, which adds work location
            to KBPE.Locations table.
            '''

            # Формирование запроса для проверки наличия такого места работы
            # в таблице KBPE.Locations.
            ##################################################################
            # Generating sql-query for checking existence of the work location
            # in KBPE.Locations table.
            local_query_form =\
                'select*from KBPE.Locations where loc_name = \'%s\';'
            local_query = local_query_form % (text)

            local_parser = mysqlScheduleParser()
            cursor = local_parser.connection.cursor()
            count = cursor.execute(local_query)
            if count == 0:
                flag = True
            else:
                flag = False
                pass

            # Формирование итогового sql-запроса.
            ##################################################################
            # Generating final sql-query.
            if flag:
                mysql_query_form =\
                    'Replace KBPE.Locations (loc_name) VALUES (\'%s\');'
                mysql_query = mysql_query_form % (text)
            else:
                mysql_query = ''
            return flag, mysql_query

        flag, mysql_query = make_query(location)
        if flag:
            try:
                local_parser = mysqlScheduleParser()
                cursor = local_parser.connection.cursor()
                cursor.execute(mysql_query)
                local_parser.connection.commit()
                local_parser.connection.close()
                return 'Новое место работы добавлено.'
            except:
                return 'Ошибка в добавлении места работы.'
        else:
            return 'Такое место работы уже есть в БД.'


    def search_user_id(self, name):
        '''
        Метод находит id сотрудника по его имени.
        ######################################################################
        By user name the method finds user id.
        '''

        local_query_form = 'select*from KBPE.Users where user_name = \'%s\';'
        local_query = local_query_form % name
        local_parser = mysqlScheduleParser()
        cursor = local_parser.connection.cursor()
        cursor.execute(local_query)
        list = cursor._rows[0]
        return list[0]


    def search_location_id(self, location):
        '''
        Метод находит id места работы по его названию.
        ######################################################################
        By work location`s name the method finds work location`s id.
        '''

        local_query_form = 'select*from KBPE.Locations where loc_name = \'%s\';'
        local_query = local_query_form % location
        local_parser = mysqlScheduleParser()
        cursor = local_parser.connection.cursor()
        cursor.execute(local_query)
        list = cursor._rows[0]
        return list[0]


    def msp_set_day_schedule(self, text):
        '''
        Метод добавляет расписание сотрудника на 1 день.
        ######################################################################
        The method adds one-day schedule for employee.
        '''

        def make_query(command_list):
            '''
            Метод формирует запрос на языке SQL, который добавит расписание
            сотрудника на 1 день.
            ##################################################################
            The method generates a SQL query, which adds one-day schedule
            for the employee.
            '''

            # Формирование запроса для проверки наличия расписания этого
            # сотрудника в этот день.
            ##################################################################
            # Generating sql-query for checking existence of the one-day
            # schedule for the employee.
            user_id = self.search_user_id(command_list[0])
            date = command_list[2]
            mysql_query_form = 'select*from %s where date = \'%s\' ' \
                               'and user_id = \'%s\';'
            local_query = mysql_query_form % ('KBPE.Schedule', date, user_id)
            local_parser = mysqlScheduleParser()
            cursor = local_parser.connection.cursor()
            count = cursor.execute(local_query)
            if count == 0:
                flag = False
                id = ''
            else:
                list = cursor._rows[0]
                flag = True
                id = list[0]

            location_id = self.search_location_id(command_list[1].lower())
            time_start = command_list[3].replace('.', ':') + ':00'
            time_finish = command_list[4].replace('.', ':') + ':00'

            # Формирование итогового sql-запроса.
            ##################################################################
            # Generating final sql-query.
            if flag:
                mysql_query_form = 'Replace %s VALUES (\'%s\', \'%s\', ' \
                                   '\'%s\', \'%s\', \'%s\', \'%s\');'
                mysql_query = mysql_query_form % ('KBPE.Schedule', id, date, user_id,
                                                  location_id, time_start, time_finish)
            else:
                mysql_query_form = 'Replace %s (date, user_id, location_id, ' \
                                   'time_start, time_finish) VALUES (\'%s\', ' \
                                   '\'%s\', \'%s\', \'%s\', \'%s\');'
                mysql_query = mysql_query_form % ('KBPE.Schedule', date, user_id,
                                                  location_id, time_start, time_finish)
            return mysql_query

        # Проверка правильности введённой команды.
        ######################################################################
        # Checking correctness of the command.
        flag, answer, command_list = self.checker.cc_set_day_input_check(text)

        # Проверка является ли день праздничным.
        ######################################################################
        # Checking whether the day is festive.
        if command_list[2] in HOLIDAYS:
            return 'Это праздничный день. Расписание не добавлено.'

        # Формирование ответного сообщения.
        ######################################################################
        # Generating final answer message.
        if flag:
            mysql_query = make_query(command_list)
            try:
                local_parser = mysqlScheduleParser()
                cursor = local_parser.connection.cursor()
                cursor.execute(mysql_query)
                local_parser.connection.commit()
                local_parser.connection.close()
                return 'Расписание успешно добавлено.'
            except:
                return 'Ошибка в добавлении расписания.'
        else:
            # Сообщение об ошибке.
            ##################################################################
            # Error message.
            return answer


    def msp_set_day_schedule_repeat(self, text):
        '''
        Метод добавляет расписание сотрудника на 1 день, определяет день
        недели, копирует это расписание во все такие же дни недели в
        ближайшие 3 месяца (например, добавляет расписание во все вторники
        начиная с сегодняшнего дня и во все дни ближайших 3 месяцев).
        ######################################################################
        The method adds one-day schedule for employee, then the method
        determines the weekday, then the method copies the one-day schedule
        for the same weekdays in the next 3 month.
        '''

        # Проверка правильности введённой команды.
        ######################################################################
        # Checking correctness of the command.
        flag, answer, list = self.checker.cc_set_day_input_check(text)

        # Проверка правильности введённой команды.
        ##################################################################
        # Checking correctness of the command.
        if flag:
            # Получаем список дат таких же дней недели в ближайшие 3 месяца.
            ##################################################################
            # Getting a list of dates for the same weekdays in the next
            # 3 month.
            same_weekday_list = self.my_searcher.cs_search_same_weekdays(list[2])
            for each in same_weekday_list:
                list[2] = each
                self.msp_set_day_schedule(list)
            return 'Расписание успешно добавлено на 3 месяца вперёд.'
        else:
            # Сообщение об ошибке.
            ##################################################################
            # Error message.
            return answer


    def msp_get_day_schedule(self, text):
        '''
        Метод получает расписание одного сотрудника в конкретный день.
        ######################################################################
        The method gets one employee`s schedule for the date.
        '''

        def make_query(command_list):
            '''
            Метод формирует запрос на языке SQL, который получит расписание
            сотрудника на 1 день.
            ##################################################################
            The method generates a SQL query, which gets one-day schedule
            for the employee.
            '''

            user_id = self.search_user_id(command_list[0])
            date = command_list[1]

            # Формирование итогового sql-запроса.
            ##################################################################
            # Generating final sql-query.
            mysql_query_form = 'select*from KBPE.Schedule ' \
                               'inner join KBPE.Locations on KBPE.Schedule.location_id = KBPE.Locations.id ' \
                               'inner join KBPE.Users on KBPE.Schedule.user_id = KBPE.Users.id where ' \
                               'user_id = \'%s\' and date = \'%s\';'
            mysql_query = mysql_query_form % (user_id, date)
            return mysql_query

        # Проверка правильности введённой команды.
        ##################################################################
        # Checking correctness of the command.
        flag, answer, list = self.checker.cc_get_day_input_check(text)

        # Формирование ответного сообщения.
        ######################################################################
        # Generating final answer message.
        if flag:
            date = list[1]
            weekday = WEEKDAYS[calendar.weekday(int(date[0:4]),
                                                int(date[5:7]),
                                                int(date[8:10]))]
            message_form = '%s %s:\n'
            message = message_form % (date, weekday)

            # Проверка является ли день праздничным.
            ##################################################################
            # Checking whether the day is festive.
            if date in HOLIDAYS:
                message += '\t\t\t-----> Это праздничный день.'
                return message

            cursor = self.connection.cursor()
            mysql_query = make_query(list)
            try:
                cursor.execute(mysql_query)
                list = cursor._rows[0]
                name = list[9]
                time_start = list[4]
                time_finish = list[5]
                place = list[7]
                self.connection.close()
                message +=\
                    '\t\t\t-----> %s работает с %s по %s. Место работы - %s.'\
                    % (str(name), str(time_start),
                       str(time_finish), str(place))
                return message
            except:
                self.connection.rollback()
                self.connection.close()
                message += '\t\t\t-----> %s не работает.' % (list[0])
                return message
        else:
            # Сообщение об ошибке.
            ##################################################################
            # Error message.
            return answer


    def msp_get_day_schedule_everybody(self, text):
        '''
        Метод получает расписание всех сотрудника в конкретный день.
        ######################################################################
        The method gets all employee`s schedule for the date.
        '''

        def make_query(date):
            '''
            Метод формирует запрос на языке SQL, который получит расписание
            всех сотрудников на 1 день.
            ##################################################################
            The method generates a SQL query, which gets one-day schedule
            for all employees.
            '''

            mysql_query_form = 'select*from KBPE.Schedule ' \
                               'inner join KBPE.Locations on KBPE.Schedule.location_id = KBPE.Locations.id ' \
                               'inner join KBPE.Users on KBPE.Schedule.user_id = KBPE.Users.id where ' \
                               'date = \'%s\';'
            mysql_query = mysql_query_form % (date)
            return mysql_query

        # Проверка правильности введённой команды.
        ##################################################################
        # Checking correctness of the command.
        answer, flag, date = self.checker.cc_check_date(True, '', text)

        # Формирование ответного сообщения.
        ######################################################################
        # Generating final answer message.
        if flag:
            weekday = WEEKDAYS[calendar.weekday(int(date[0:4]),
                                            int(date[5:7]),
                                            int(date[8:10]))]
            message_form = '%s %s:\n'
            message = message_form % (date, weekday)
            mysql_query = make_query(date)
            if date in HOLIDAYS:
                message += '\t\t\t-----> Это праздничный день.'
                return message
            try:
                local_parser = mysqlScheduleParser()
                cursor = local_parser.connection.cursor()
                count = cursor.execute(mysql_query)
                if count == 0:
                    message += '\t\t\t-----> В указанный день никто не работает. \n'
                    return message
                for each in cursor._rows:
                    message_plus_form = '\t\t\t-----> %s работает с %s по %s. Место работы - %s. \n'
                    message += message_plus_form % (str(each[9]), str(each[4]), str(each[5]), str(each[7]))
                return message
            except:
                return 'Ошибка в выполнении запроса.'
        else:
            # Сообщение об ошибке.
            ##################################################################
            # Error message.
            return answer


    def msp_get_week_schedule(self, week, text):
        '''
        Метод получает расписание одного сотрудника в эту неделю.
        ######################################################################
        The method gets one employee`s schedule in this week.
        '''

        # Проверка правильности введённой команды.
        ##################################################################
        # Checking correctness of the command.
        answer, flag = self.checker.cc_check_name(True, '', text)

        # Формирование ответного сообщения.
        ######################################################################
        # Generating final answer message.
        if flag:
            # Формирование списка дат всех дней этой недели.
            ##################################################################
            # Generating list of dates of all days of the week.
            date_list = self.my_searcher.cs_search_days_week(week)
            result_list = []

            # Получение расписание каждого дня из списка.
            ##################################################################
            # Getting a schedule for each date in date_list.
            for each in date_list:
                local_parser = mysqlScheduleParser()
                command = text + ' ' + each
                answer = local_parser.msp_get_day_schedule(command)
                result_list.append(answer)
            return result_list
        else:
            # Сообщение об ошибке.
            ##################################################################
            # Error message.
            return [answer]


    def msp_get_week_schedule_everybody(self, week):
        '''
        Метод получает расписание всех сотрудников в эту неделю.
        ######################################################################
        The method gets all employee`s schedule in this week.
        '''

        # Формирование списка дат всех дней этой недели.
        ##################################################################
        # Generating list of dates of all days of the week.
        date_list = self.my_searcher.cs_search_days_week(week)
        result_list = []

        # Получение расписание каждого дня из списка.
        ##################################################################
        # Getting a schedule for each date in date_list.
        for each in date_list:
            local_parser = mysqlScheduleParser()
            answer = local_parser.msp_get_day_schedule_everybody(each)
            result_list.append(answer)
        return result_list
