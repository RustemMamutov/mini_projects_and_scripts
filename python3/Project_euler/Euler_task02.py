a = 1
b = 2
summ = 2
while b<=4000000:
    temp = a + b
    a = b
    b = temp
    if (b%2==0):
        summ += b
print(summ)