import datetime
import calendar

class calendarSearcher():
    '''
    Класс, который работает с календарём.
    ##########################################################################
    The class, which works with calendar.
    '''

    def __init__(self):
        pass


    def cs_search_days_week(self, week):
        '''
        Метод, который находит все даты в указанной неделе.
        ######################################################################
        The method, which searches all days in the week.
        '''

        def parse_month(year, month, week1, list1):
            while month <=12:
                days_count = calendar.monthrange(year, month)[1]
                this_month_max_week = datetime.date(year,
                                                    month,
                                                    days_count).isocalendar()[1]

                # Сравнение недели с максимальной неделей этого месяца.
                ##############################################################
                # Comparison of the week with maximum week of this month.
                if (month!=12 and this_month_max_week < week1):
                    pass
                else:
                    i = 1
                    while i <= days_count:
                        local_week = datetime.date(year,
                                                   month,
                                                   i).isocalendar()[1]
                        if local_week == week1:
                            # Формируется дата в формате гггг.мм.дд.
                            ##################################################
                            # Forming date in format yyyy.mm.dd.
                            date = str(year) + '.' + str(month)
                            if (len(str(month))==1):
                                date = str(year) + '.0' + str(month)
                            day = str(i)
                            if (len(day)==1):
                                day = '0' + day
                            date += '.' + day
                            list1.append(date)
                        i += 1
                        if len(list1) == 7:
                            return list1
                month += 1
            return list1

        current_year = datetime.datetime.now().year
        week_days_list = []

        # Особый алгоритм для 1-ой недели.
        # В питоне 53-ая неделя года считается за 1-ую неделю следующего года.
        # Поэтому при составлении списка дат сначала вызывается метод
        # parse_month для последнего месяца ПРЕДЫДУЩЕГО года, а потом для
        # первого месяца текущего года.
        ######################################################################
        # A special algorithm for the 1st week.
        # In python3 53rd week of current year is considered as the 1st week
        # on the next year. For the reason firstly the method parse_month is
        # called for the last month of previous year and then for 1-st month
        # of the current year.
        if week == 1:
            local_list = parse_month(current_year-1, 12, 1, [])
            week_days_list = parse_month(current_year, 1, 1, local_list)
        elif 2<= week <= 52:
            week_days_list = parse_month(current_year, 1, week, [])
        else:
            pass
        return week_days_list


    def cs_search_days_month(self, month):
        '''
        Метод, который находит все даты в указанном месяце.
        ######################################################################
        The method, which searches all days in the month.
        '''

        month_days_list = []

        # Номер текущего года.
        ######################################################################
        # Current year number.
        current_year = datetime.datetime.now().year

        # Количество дней в указанном месяце текущего года.
        ######################################################################
        # Count of days in current month of current year.
        range = calendar.monthrange(current_year, month)
        i=1
        month1 = str(month)
        if len(month1)==1:
            month1 = '0' + month1
        while i <= range[1]:

            day = str(i)
            if (len(day)==1):
                date = month1 + '.0' + day
            else:
                date = month1 + '.' + day
            date = str(current_year) + '.' + date
            month_days_list.append(date)
            i += 1
        # Список всех дат указанного месяца текущего года.
        ######################################################################
        # List of all dates of the month of current year.
        return month_days_list


    def cs_search_same_weekdays(self, date):
        '''
        Метод, который находит в следующие 3 месяца все даты, в которые
        день недели совпадает с текущим (например ищет даты всех вторников).
        ######################################################################
        The method, which searches in the next 3 month all dates, where the
        weekday is the same as current (for example, it searches for dates of
        all Tuesdays).
        '''

        year = int(date[0:4])
        start_month = int(date[5:7])
        start_day = int(date[8:10])
        # Исходный день недели.
        ######################################################################
        # Initial weekday.
        base_weekday = calendar.weekday(year, start_month, start_day)
        same_weekdays_list = []
        month = start_month
        end_month = start_month + 3
        if end_month > 12:
            end_month = 12

        while month <= end_month:
            # Количество дней в этом месяце.
            ##################################################################
            # Count of days in the month.
            range = calendar.monthrange(year, month)
            i = 1
            if month == start_month:
                i = start_day
            while i <= range[1]:
                # Текущий день недели.
                ##############################################################
                # Current weekday.
                local_weekday = calendar.weekday(year, month, i)
                if (base_weekday == local_weekday):
                    # Формирование даты в виде гггг.мм.дд.
                    ##########################################################
                    # Forming date in format yyyy.mm.dd.
                    date_form = '%s.%s.%s'
                    day = str(i)
                    if (len(str(i)) == 1):
                        day = '0' + str(i)
                    month1 = str(month)
                    if (len(month1) == 1):
                        month1 = '0' + month1
                    full_date = date_form % (date[0:4], month1, day)
                    same_weekdays_list.append(full_date)
                i += 1
            month += 1

        return same_weekdays_list
