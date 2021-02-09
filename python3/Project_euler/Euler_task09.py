import math

a = 3
b = 4
c = 5

flag = False
for i in range(a, 333):
    for j in range(i+1, 1000-i):
        z = math.sqrt(i**2 + j**2)
        if z.is_integer():
            if i + j + z == 1000:
                print("{}; {}; {}; ".format(i, j, int(z)) +
                      " SUMM = 1000; composion = " + str(i*j*z))
                flag = True
        if flag:
            break
    if flag:
        break
