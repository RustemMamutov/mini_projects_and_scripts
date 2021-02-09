import os
import re


# функция ищет файлы с заданным расширением в текущей и во всех вложенных папках
# the function searches files in current dir and in all subdirectories
def filesearch(dictionary, path):
    pathlist = os.listdir(path)
    for eachname in pathlist:
        if os.path.isfile(os.path.join(path, eachname)):
            if eachname.endswith('Makefile'):
                fullpath = path + "\\" + eachname
                dictionary[fullpath] = eachname
        elif os.path.isdir(os.path.join(path, eachname)):
            newpath = path + "\\" + eachname
            filesearch(dictionary, newpath)


# функция преобразует файл в словарь с ключами из номеров строк
# the function converts file into dictionary. Line numbers are keys
def texttodict(fullpath):
        i = 0
        dictionary = dict()
        for eachline in open(os.path.abspath(fullpath), 'r'):
            i += 1
            dictionary[i] = eachline
        return dictionary


curdir_path = input("Введите адрес папки: ")
resultfilelist = dict()
filesearch(resultfilelist, curdir_path)
textToSearch = 'usr/lib/qt-3.3'
textToReplace = 'usr/share/qt3'


for each in resultfilelist:
    dicttextfile = texttodict(each)
    dicttextfile1 = dict()
    i = 1
    for eachline in dicttextfile:
        if re.search(textToSearch, dicttextfile[eachline]):
            dicttextfile1[i] = dicttextfile[eachline].replace(textToSearch, textToReplace)
        else:
            dicttextfile1[i] = dicttextfile[eachline]
        i += 1

    file = open(each + '1', 'w')
    for eachline1 in dicttextfile1:
        file.write(dicttextfile1[eachline1])
        # print(eachline1, dicttextfile1[eachline1], end='')
