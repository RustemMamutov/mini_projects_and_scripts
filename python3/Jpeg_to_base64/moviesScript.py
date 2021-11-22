import os
import base64
from collections import namedtuple
from datetime import datetime as dt
from datetime import timedelta as td

movie_info = namedtuple("movie_info", "id movie_name movie_time start_date end_date")
global_path = "C:/Users/Rustem/PycharmProjects/mini_projects_and_scripts/python3/Jpeg_to_base64"

movies = {
    1: movie_info(1, "Т 34", td(hours=2, minutes=19), dt(2019, 1, 1), dt(2019, 1, 31)),
    2: movie_info(2, "Мэри Поппинс возвращается", td(hours=2, minutes=10), dt(2019, 1, 3), dt(2019, 2, 3)),
    3: movie_info(3, "Крид 2", td(hours=2, minutes=10), dt(2019, 1, 3), dt(2019, 2, 3)),
    4: movie_info(4, "Стекло", td(hours=2, minutes=9), dt(2019, 1, 17), dt(2019, 2, 17)),
    5: movie_info(5, "Зеленая книга", td(hours=2, minutes=10), dt(2019, 1, 24), dt(2019, 2, 24)),
    6: movie_info(6, "Завод", td(hours=1, minutes=49), dt(2019, 2, 7), dt(2019, 3, 7)),
    7: movie_info(7, "Алита: боевой ангел", td(hours=2, minutes=1), dt(2019, 2, 14), dt(2019, 3, 14)),
    8: movie_info(8, "Власть", td(hours=2, minutes=12), dt(2019, 2, 21), dt(2019, 3, 21)),
    9: movie_info(9, "Наркокурьер", td(hours=1, minutes=56), dt(2019, 2, 28), dt(2019, 3, 28)),
    10: movie_info(10, "Капитан Марвел", td(hours=2, minutes=3), dt(2019, 3, 7), dt(2019, 4, 7)),
    11: movie_info(11, "Рожденный стать королем", td(hours=2, minutes=0), dt(2019, 3, 14), dt(2019, 4, 14)),
    12: movie_info(12, "Балканский рубеж", td(hours=2, minutes=31), dt(2019, 3, 21), dt(2019, 4, 21)),
    13: movie_info(13, "Дамбо", td(hours=1, minutes=52), dt(2019, 3, 28), dt(2019, 4, 28)),
    14: movie_info(14, "Пляжный бездельник", td(hours=1, minutes=35), dt(2019, 3, 28), dt(2019, 4, 28)),
    15: movie_info(15, "Шазам!", td(hours=2, minutes=12), dt(2019, 4, 4), dt(2019, 5, 4)),
    16: movie_info(16, "Хеллбой", td(hours=2, minutes=0), dt(2019, 4, 11), dt(2019, 5, 11)),
    17: movie_info(17, "После", td(hours=1, minutes=45), dt(2019, 4, 18), dt(2019, 5, 18)),
    18: movie_info(18, "Игры разумов", td(hours=2, minutes=4), dt(2019, 4, 25), dt(2019, 5, 25)),
    19: movie_info(19, "Большое путешествие", td(hours=1, minutes=20), dt(2019, 4, 27), dt(2019, 5, 27)),
    20: movie_info(20, "Мстители: Финал", td(hours=3, minutes=1), dt(2019, 4, 29), dt(2019, 5, 29)),
    21: movie_info(21, "В метре друг от друга", td(hours=1, minutes=56), dt(2019, 5, 1), dt(2019, 5, 31)),
    22: movie_info(22, "Братство", td(hours=1, minutes=53), dt(2019, 5, 10), dt(2019, 6, 10)),
    23: movie_info(23, "Джон Уик 3", td(hours=2, minutes=10), dt(2019, 5, 16), dt(2019, 6, 16)),
    24: movie_info(24, "Покемон. Детектив Пикачу", td(hours=1, minutes=44), dt(2019, 5, 16), dt(2019, 6, 16)),
    25: movie_info(25, "Алладин", td(hours=2, minutes=8), dt(2019, 5, 23), dt(2019, 6, 23)),
    26: movie_info(26, "Люди Икс: Тёмный Феникс", td(hours=1, minutes=54), dt(2019, 6, 6), dt(2019, 7, 6)),
    27: movie_info(27, "Люди в черном: интернэшнл", td(hours=1, minutes=55), dt(2019, 6, 12), dt(2019, 7, 12)),
    28: movie_info(28, "История игрушек 4", td(hours=1, minutes=40), dt(2019, 6, 20), dt(2019, 7, 20)),
    29: movie_info(29, "Дылда", td(hours=2, minutes=19), dt(2019, 6, 20), dt(2019, 7, 20)),
    30: movie_info(30, "Курск", td(hours=1, minutes=58), dt(2019, 6, 27), dt(2019, 7, 27)),
    31: movie_info(31, "Человек паук: Вдали от дома", td(hours=2, minutes=9), dt(2019, 7, 4), dt(2019, 8, 4)),
    32: movie_info(32, "Паразиты", td(hours=2, minutes=12), dt(2019, 7, 4), dt(2019, 7, 4)),
    33: movie_info(33, "Анна", td(hours=1, minutes=40), dt(2019, 7, 11), dt(2019, 8, 11)),
    34: movie_info(34, "Король лев", td(hours=1, minutes=58), dt(2019, 7, 18), dt(2019, 8, 18)),
    35: movie_info(35, "Солнцестояние", td(hours=2, minutes=18), dt(2019, 7, 18), dt(2019, 8, 18)),
    36: movie_info(36, "Форсаж: Хоббс и Шоу", td(hours=2, minutes=16), dt(2019, 8, 1), dt(2019, 9, 30)),
    37: movie_info(37, "Однажды... в Голливуде", td(hours=2, minutes=40), dt(2019, 8, 8), dt(2019, 9, 8)),
    38: movie_info(38, "Angry Birds в кино 2", td(hours=1, minutes=37), dt(2019, 8, 15), dt(2019, 9, 15)),
    39: movie_info(39, "Падение ангела", td(hours=2, minutes=1), dt(2019, 8, 22), dt(2019, 9, 22)),
    40: movie_info(40, "Я иду искать", td(hours=1, minutes=34), dt(2019, 8, 29), dt(2019, 9, 29)),
    41: movie_info(41, "Оно 2", td(hours=2, minutes=50), dt(2019, 9, 5), dt(2019, 10, 5)),
    42: movie_info(42, "Щегол", td(hours=2, minutes=29), dt(2019, 9, 12), dt(2019, 10, 12)),
    43: movie_info(43, "Рэмбо:Последняя кровь", td(hours=1, minutes=39), dt(2019, 9, 19), dt(2019, 10, 19)),
    44: movie_info(44, "К звездам", td(hours=2, minutes=4), dt(2019, 9, 26), dt(2019, 10, 26)),
    45: movie_info(45, "Герой", td(hours=2, minutes=12), dt(2019, 9, 26), dt(2019, 10, 26)),
    46: movie_info(46, "Джокер", td(hours=2, minutes=2), dt(2019, 10, 3), dt(2019, 11, 3)),
    47: movie_info(47, "Эверест", td(hours=1, minutes=37), dt(2019, 10, 3), dt(2019, 11, 3)),
    48: movie_info(48, "Гемини", td(hours=1, minutes=57), dt(2019, 10, 10), dt(2019, 11, 10)),
    49: movie_info(49, "Малефисента: Владычеца тьмы", td(hours=1, minutes=58), dt(2019, 10, 17), dt(2019, 11, 17)),
    50: movie_info(50, "Текст", td(hours=2, minutes=12), dt(2019, 10, 24), dt(2019, 11, 24)),
    51: movie_info(51, "Докстор сон", td(hours=2, minutes=3), dt(2019, 11, 7), dt(2019, 12, 7)),
    52: movie_info(52, "Во все тяжкое", td(hours=1, minutes=31), dt(2019, 11, 7), dt(2019, 12, 7)),
    53: movie_info(53, "FORD против FERRARI", td(hours=2, minutes=32), dt(2019, 11, 14), dt(2019, 12, 14)),
    54: movie_info(54, "Аванпост", td(hours=2, minutes=32), dt(2019, 11, 21), dt(2019, 12, 21)),
    55: movie_info(55, "Достать ножи", td(hours=2, minutes=10), dt(2019, 11, 28), dt(2019, 12, 28)),
    56: movie_info(56, "Холодное сердце 2", td(hours=1, minutes=43), dt(2019, 11, 28), dt(2019, 12, 28)),
    57: movie_info(57, "21 мост", td(hours=1, minutes=39), dt(2019, 12, 5), dt(2020, 1, 5)),
    58: movie_info(58, "Сиротский бруклин", td(hours=2, minutes=24), dt(2019, 12, 5), dt(2020, 1, 5)),
    59: movie_info(59, "Джуманджи:Новый уровень", td(hours=2, minutes=3), dt(2019, 12, 12), dt(2020, 1, 12)),
    60: movie_info(60, "Звездные войны: Скайуокер. Восход", td(hours=2, minutes=22), dt(2019, 12, 19), dt(2020, 1, 19)),
    61: movie_info(61, "Холоп", td(hours=1, minutes=49), dt(2019, 12, 26), dt(2020, 1, 26)),
    62: movie_info(62, "Вторжение", td(hours=2, minutes=14), dt(2020, 1, 1), dt(2020, 1, 31)),
    63: movie_info(63, "Камуфляж и шпионаж", td(hours=1, minutes=42), dt(2020, 1, 9), dt(2020, 2, 9)),
    64: movie_info(64, "Маяк", td(hours=1, minutes=50), dt(2020, 1, 16), dt(2020, 2, 16)),
    65: movie_info(65, "Плохие парни навсегда", td(hours=2, minutes=4), dt(2020, 1, 23), dt(2020, 2, 23)),
    66: movie_info(66, "1917", td(hours=1, minutes=59), dt(2020, 1, 30), dt(2020, 2, 28)),
    67: movie_info(67, "Хищные птицы: Потрясающая история Харли Квинн", td(hours=1, minutes=49), dt(2020, 2, 6), dt(2020, 3, 6)),
    68: movie_info(68, "Джентельмены", td(hours=1, minutes=53), dt(2020, 2, 13), dt(2020, 3, 13)),
    69: movie_info(69, "Скандал", td(hours=1, minutes=49), dt(2020, 2, 13), dt(2020, 3, 13)),
    70: movie_info(70, "Лёд 2", td(hours=2, minutes=12), dt(2020, 2, 14), dt(2020, 3, 14)),
    71: movie_info(71, "Соник в кино", td(hours=1, minutes=40), dt(2020, 2, 20), dt(2020, 3, 20)),
    72: movie_info(72, "Человек-неведимка", td(hours=2, minutes=5), dt(2020, 3, 5), dt(2020, 4, 5)),
    73: movie_info(73, "Вперед", td(hours=1, minutes=42), dt(2020, 3, 3), dt(2020, 4, 5)),
    74: movie_info(74, "Бладшот", td(hours=1, minutes=49), dt(2020, 3, 12), dt(2020, 4, 12)),
    75: movie_info(75, "Тайная жизнь", td(hours=3, minutes=0), dt(2020, 3, 19), dt(2020, 4, 19)),
    76: movie_info(76, "Тролли.Мировой тур", td(hours=1, minutes=30), dt(2020, 3, 19), dt(2020, 4, 19)),
    77: movie_info(77, "Горы,солнце и любовь", td(hours=1, minutes=38), dt(2020, 4, 2), dt(2020, 5, 2)),
    78: movie_info(78, "Отель для самоубийц", td(hours=1, minutes=30), dt(2020, 4, 16), dt(2020, 5, 16)),
    79: movie_info(79, "Прекрасные лжецы", td(hours=1, minutes=20), dt(2020, 4, 23), dt(2020, 5, 23)),
    80: movie_info(80, "Запретная кухня", td(hours=1, minutes=25), dt(2020, 4, 30), dt(2020, 5, 30)),
    81: movie_info(81, "Прощай", td(hours=1, minutes=51), dt(2020, 5, 14), dt(2020, 6, 14)),
    82: movie_info(82, "Странники терпенья", td(hours=1, minutes=45), dt(2020, 5, 14), dt(2020, 6, 14)),
    83: movie_info(83, "Звонок", td(hours=1, minutes=52), dt(2020, 5, 21), dt(2020, 6, 21)),
    84: movie_info(84, "Книга моря", td(hours=1, minutes=25), dt(2020, 5, 21), dt(2020, 6, 21)),
    85: movie_info(85, "Мы умираем молодыми", td(hours=1, minutes=32), dt(2020, 6, 4), dt(2020, 7, 4)),
    86: movie_info(86, "Дикая роза", td(hours=1, minutes=42), dt(2020, 6, 11), dt(2020, 7, 11)),
    87: movie_info(87, "Где-то там", td(hours=1, minutes=34), dt(2020, 6, 16), dt(2020, 7, 16)),
    88: movie_info(88, "Убийства по открыткам", td(hours=1, minutes=44), dt(2020, 6, 25), dt(2020, 7, 25)),
    89: movie_info(89, "Мисс Плохое поведение", td(hours=1, minutes=47), dt(2020, 7, 6), dt(2020, 8, 6)),
    90: movie_info(90, "Основатель", td(hours=1, minutes=55), dt(2020, 7, 23), dt(2020, 8, 23)),
    91: movie_info(91, "Ловушка разума", td(hours=1, minutes=28), dt(2020, 7, 23), dt(2020, 8, 23)),
    92: movie_info(92, "Махинаторы", td(hours=1, minutes=31), dt(2020, 7, 30), dt(2020, 8, 30)),
    93: movie_info(93, "Мой шпион", td(hours=1, minutes=40), dt(2020, 8, 1), dt(2020, 8, 31)),
    94: movie_info(94, "Побег из Претории", td(hours=1, minutes=46), dt(2020, 8, 1), dt(2020, 8, 31)),
    95: movie_info(95, "Неистовый", td(hours=1, minutes=30), dt(2020, 8, 6), dt(2020, 9, 6)),
    96: movie_info(96, "Форпост", td(hours=2, minutes=3), dt(2020, 8, 13), dt(2020, 9, 13)),
    97: movie_info(97, "Гренландия", td(hours=2, minutes=0), dt(2020, 8, 20), dt(2020, 9, 20)),
    98: movie_info(98, "Агент Ева", td(hours=1, minutes=37), dt(2020, 8, 20), dt(2020, 9, 20)),
    99: movie_info(99, "Вратарь галактики", td(hours=1, minutes=58), dt(2020, 8, 27), dt(2020, 9, 27)),
    100: movie_info(100, "Новые мутанты", td(hours=1, minutes=39), dt(2020, 9, 3), dt(2020, 10, 3)),
    101: movie_info(101, "Довод", td(hours=2, minutes=30), dt(2020, 9, 3), dt(2020, 10, 3)),
    102: movie_info(102, "Мулан", td(hours=2, minutes=0), dt(2020, 9, 10), dt(2020, 10, 10)),
    103: movie_info(103, "После.Глава 2", td(hours=1, minutes=47), dt(2020, 9, 17), dt(2020, 10, 17)),
    104: movie_info(104, "Стрельцов", td(hours=1, minutes=41), dt(2020, 9, 24), dt(2020, 10, 24)),
    105: movie_info(105, "Капоне.Лицо со шрамом", td(hours=1, minutes=44), dt(2020, 10, 1), dt(2020, 10, 31)),
    106: movie_info(106, "Гудбай,Америка", td(hours=1, minutes=45), dt(2020, 10, 8), dt(2020, 11, 8)),
    107: movie_info(107, "KITOBOY", td(hours=1, minutes=33), dt(2020, 10, 8), dt(2020, 11, 8)),
    108: movie_info(108, "Доктор Лиза", td(hours=2, minutes=0), dt(2020, 10, 22), dt(2020, 11, 22)),
    109: movie_info(109, "Ведьмы", td(hours=1, minutes=46), dt(2020, 10, 29), dt(2020, 11, 29)),
    110: movie_info(110, "Выбивая долги", td(hours=1, minutes=35), dt(2020, 11, 4), dt(2020, 12, 4)),
    111: movie_info(111, "Побочный эффект", td(hours=1, minutes=33), dt(2020, 11, 5), dt(2020, 12, 5)),
    112: movie_info(112, "Еще по одной", td(hours=1, minutes=57), dt(2020, 11, 12), dt(2020, 12, 12)),
    113: movie_info(113, "Афера по-голливудски", td(hours=1, minutes=44), dt(2020, 11, 19), dt(2020, 12, 19)),
    114: movie_info(114, "Искуственный интелект", td(hours=1, minutes=46), dt(2020, 11, 26), dt(2020, 12, 26)),
    115: movie_info(115, "Человек из подольска", td(hours=1, minutes=32), dt(2020, 11, 26), dt(2020, 12, 26)),
    116: movie_info(116, "Трое", td(hours=2, minutes=7), dt(2020, 12, 3), dt(2021, 1, 3)),
    117: movie_info(117, "Неадекватные люди 2", td(hours=2, minutes=15), dt(2020, 12, 10), dt(2021, 1, 10)),
    118: movie_info(118, "На твоей волне", td(hours=1, minutes=36), dt(2020, 12, 17), dt(2021, 1, 17)),
    119: movie_info(119, "Семейка Крудс: Новоселье", td(hours=1, minutes=35), dt(2020, 12, 24), dt(2021, 1, 24)),
    120: movie_info(120, "Конь Юлий и большие скачки", td(hours=1, minutes=17), dt(2020, 12, 31), dt(2021, 1, 31))
}

resultDict = {}

images_path = "{0}/{1}".format(global_path, "images")
for each_file in os.listdir(images_path):
    movie_id = int(each_file.split("-")[0])
    movie_name = movies[movie_id].movie_name
    image = open("{}/{}".format(images_path, each_file), 'rb')
    image_read = image.read()
    image_64_encode = "data:image/jpeg;base64," + str(base64.b64encode(image_read))[2:-1]
    if movie_id not in resultDict:
        resultDict[movie_id] = "{0}*{1}*{2}".format(movie_id, movie_name, image_64_encode)
    else:
        resultDict[movie_id] = "{0}|{1}".format(resultDict[movie_id], image_64_encode)

with open("{0}/{1}".format(global_path, "movies.csv"), "w", encoding="UTF8") as file:
    file.write('"id"*"name"*"base64_images"\n')
    for each in resultDict.values():
        file.write(each + "\n")
    print()


