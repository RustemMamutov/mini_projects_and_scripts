i = 1
amount = 0
while i<1000:
    if (i%3==0):
        amount += i
    elif (i%5==0):
        amount += i
    i += 1
print(amount)
