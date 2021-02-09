# coding: utf-8

'''
Этот код предназначен для скачивания документа Google sheet.
Раз в 30 минут код обновляет файл New.xlsx (скачивает
документ Google sheet и называет его New.xlsx - таким
образом происходит обновление файла New.xlsx).
В период с 0 до 2 часов код обновляет файл Old.xlsx.
После этого код обновляет файл New.xlsx.
В этот момент файлы Old.xlsx и New.xlsx являются одинаковыми.
'''

from requests import get
import time
import os

url_file = 'TO DOWNLOAD EXCEL FILE PUT YOUR URL HERE'

def download(url, file_name):
    '''
    Функция, которая скачивает файл по переданной ссылке и
    присваивает скачанному файлу имя, переданное в функцию.
    '''
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

while True:
    # текущее время (только часы).
    current_hour = time.strftime("%H")
    if(0<int(current_hour)<2):
        # Обновление файла Old.xlsx.
        download(url_file, 'Old.xlsx')
        # Обновление файла New.xlsx.
        download(url_file, 'New.xlsx')
        # Пауза 1 час
        time.sleep(3600)
    # Обновление файла New.xlsx.
    download(url_file, 'New.xlsx')
    # Пауза 30 минут
    time.sleep(1800)
