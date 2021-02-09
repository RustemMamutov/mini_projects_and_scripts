import slackclient
import time
import datetime
from mysqlScheduleParser import mysqlScheduleParser
from constants import SLACK_BOT_TOKEN

slack_bot = slackclient.SlackClient(SLACK_BOT_TOKEN)

def show_commands(channel):
    '''
    Функция выводит команды.
    ##########################################################################
    The function outputs the commands.
    '''

    slack_bot.rtm_send_message(channel,
'''
adduser + имя - добавить сотрудника
addloc + название - добавить место работы
setd + имя + место работы + дата + время начала + время конца - добавить расписание сотрудника
setd + имя + место работы + дата + время начала + время конца + base
- добавить расписание сотрудника и скопировать этот день недели на ближайшие 3 месяца
getd + имя + дата - показать расписание сотрудника по дате
getd + дата - показать расписание всех сотрудников по дате
getw + имя - показать расписание сотрудника на этой неделе
getw - показать расписание всех сотрудников на этой неделе
getnw + имя - показать расписание сотрудника на следующей неделе
getnw - показать расписание всех сотрудников на следующей неделе
''')


def show_commands_examples(channel):
    '''
    Функция выводит примеры команд.
    ##########################################################################
    The function outputs the commands examples.
    '''

    slack_bot.rtm_send_message(channel,
'''
adduser Richard - добавить сотрудника
addloc Bali - добавить место работы
setd Victor office 2018.03.31 10.00 19.00 - добавить расписание сотрудника
setd Victor office 2018.03.31 10.00 19.00 base - добавить расписание
сотрудника и скопировать этот день недели на ближайшие 3 месяца
getd Roman 2018.03.31 - показать расписание сотрудника по дате
getd 2018.03.31 - показать расписание всех сотрудников по дате
getw Roman - показать расписание сотрудника на этой неделе
getw - показать расписание всех сотрудников на этой неделе
getnw Roman - показать расписание сотрудника на следующей неделе
getnw - показать расписание всех сотрудников на следующей неделе
''')


def main():
    '''
    Главная функция. Распознаёт команды и выполняет соответствующие действия.
    ##########################################################################
    The main function.
    It identifies commands and performs appropriate actions.
    '''

    if not slack_bot.rtm_connect():
        raise Exception("Couldn't connect to slack.")

    while True:
        for slack_event in slack_bot.rtm_read():
            if not slack_event.get('type') == 'message':
                continue

            message = slack_event.get('text')
            channel = slack_event.get("channel")

            try:
                my_parser = mysqlScheduleParser()

                # Показ всех команд бота.
                ##############################################################
                # Showing all bot`s commands.
                if ('show' == message):
                    show_commands(channel)

                # Показ образцов всех команд бота.
                ##############################################################
                # Showing all bot`s commands examples.
                elif ('examples' == message):
                    show_commands_examples(channel)

                # Добавить нового сотрудника.
                ##############################################################
                # Add new employee.
                elif ('adduser' in message):
                    text = message[8:]
                    my_parser.msp_add_employee(text)

                # Добавить новое место работы.
                ##############################################################
                # Add new work location.
                elif ('addloc' in message):
                    text = message[7:]
                    my_parser.msp_add_location(text)

                # Добавляет расписание в БД.
                ##############################################################
                # Adds a schedule to the database.
                elif ('setd' in message):
                    # Команда без 'setd'.
                    ##########################################################
                    # Command without 'setd'.
                    text = message[5:]
                    local_list = text.split(' ')
                    last_word = len(local_list) - 1

                    # Поиск ключевого слова 'base'. Если ключевое слово
                    # найдено, то расписание этого дня копируется на
                    # ближайшие 3 месяца.
                    ##########################################################
                    # Searching for keyword 'base'. If it is found, the
                    # current day`s schedule is copied for the next 3 month.
                    if (local_list[last_word] == 'base'):
                        text = text[:len(text)-5]
                        answer = my_parser.msp_set_day_schedule_repeat(text)
                    else:
                        answer = my_parser.msp_set_day_schedule(text)
                    slack_bot.rtm_send_message(channel, answer)
                    slack_bot.rtm_send_message(channel,
                                               'show - показать все команды\n'
                                    'examples - показать образцы все команд')

                # Получение расписание одного дня из БД либо для 1 сотрудника,
                # либо для всех.
                ##############################################################
                # Getting one-day schedule from the database for only one
                # employee or for all employees.
                elif ('getd' in message):
                    # Команда без 'getd'.
                    ##########################################################
                    # Command without 'getd'.
                    text = message[5:]

                    # Проверка кол-ва слов в сообщении. Если 2 слова,
                    # то идёт поиск по всем сотрудникам.
                    ##########################################################
                    # Checking count of words in message. If count = 2 there
                    # is a search for all employees.
                    if len(message.split(' ')) == 2:
                        answer =\
                            my_parser.msp_get_day_schedule_everybody(text)
                        slack_bot.rtm_send_message(channel, answer)
                    else:
                        answer = my_parser.msp_get_day_schedule(text)
                        slack_bot.rtm_send_message(channel, answer)
                    slack_bot.rtm_send_message(channel,
                                               'show - показать все команды\n'
                                    'examples - показать образцы все команд')


                # Получает расписание текущей недели из БД
                # либо для 1 сотрудника, либо для всех.
                ##############################################################
                # Gets the current week`s schedule from the database
                # for only one employee or for all employees.
                elif ('getw' in message):
                    now = datetime.datetime.now()
                    week = int(datetime.date(now.year,
                                             now.month,
                                             now.day).isocalendar()[1])

                    # Команда без 'getw'.
                    ##########################################################
                    # Command without 'getw'.
                    text = message[5:]

                    # Проверка кол-ва слов в сообщении. Если 1 слово,
                    # то идёт поиск по всем сотрудникам.
                    ##########################################################
                    # Checking count of words in message. If count = 1 there
                    # is a search for all employees.
                    if message == 'getw':
                        answer_list = \
                            my_parser.msp_get_week_schedule_everybody(week)
                        for each in answer_list:
                            slack_bot.rtm_send_message(channel, each)
                    elif len(message.split(' ')) != 1:
                        answer_list = \
                            my_parser.msp_get_week_schedule(week, text)
                        for each in answer_list:
                            slack_bot.rtm_send_message(channel, each)
                    else:
                        slack_bot.rtm_send_message(channel,
                                                   'Ошибка в команде')
                    slack_bot.rtm_send_message(channel,
                                               'show - показать все команды\n'
                                    'examples - показать образцы все команд')
					

                # Получает расписание слудующей недели из БД
                # либо для 1 сотрудника, либо для всех.
                ##############################################################
                # Gets the next week`s schedule from the database
                # for only one employee or for all employees.
                elif ('getnw' in message):
                    now = datetime.datetime.now()
                    # Номер текущей недели.
                    ##########################################################
                    # Current week number.
                    week = int(datetime.date(now.year,
                                             now.month,
                                             now.day).isocalendar()[1])

                    # Номер следующей недели.
                    ##########################################################
                    # Next week number.
                    if week == 52:
                        week = 1
                    else:
                        week += 1

                    # Команда без 'getnw'.
                    ##########################################################
                    # Command without 'getnw'.
                    text = message[6:]

                    # Проверка кол-ва слов в сообщении. Если 1 слово,
                    # то идёт поиск по всем сотрудникам.
                    ##########################################################
                    # Checking count of words in message. If count = 1 there
                    # is a search for all employees.
                    if message == 'getnw':
                        answer_list = \
                            my_parser.msp_get_week_schedule_everybody(week)
                        for each in answer_list:
                            slack_bot.rtm_send_message(channel, each)
                    elif len(message.split(' ')) != 1:
                        answer_list = \
                            my_parser.msp_get_week_schedule(week, text)
                        for each in answer_list:
                            slack_bot.rtm_send_message(channel, each)
                    else:
                        slack_bot.rtm_send_message(channel,
                                                   'Ошибка в команде')
                    slack_bot.rtm_send_message(channel,
                                               'show - показать все команды\n'
                                    'examples - показать образцы все команд')
                else:
                    if (channel == "C9BP9J67N"):
                        pass
                    else:
                        slack_bot.rtm_send_message(channel,
                                                   'Неизвестная команда.\n'
                                                   'show - показать все команды\n'
                                        'examples - показать образцы все команд')
            except:
                slack_bot.rtm_send_message(channel,
                                'Произошла ошибка. Не делайте так больше.')


        # Остановка на 1 секунду.
        ######################################################################
        # Sleep for a second.
        time.sleep(1)


if __name__ == '__main__':
    main()
