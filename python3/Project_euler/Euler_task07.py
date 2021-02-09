list = [2,3,5,7,11,13]
i=14
length = 6
while length<10001:
    flag = True
    for each in list:
        if i % each == 0:
            flag = False
            break
    if flag:
        list.append(i)
        length = len(list)
    i += 1

print(length)
print(list[length-1])
