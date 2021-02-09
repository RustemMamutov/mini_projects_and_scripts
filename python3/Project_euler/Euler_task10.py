from datetime import datetime
import math


def prime_sum_1(number):
    prime_list = [2]
    time1 = datetime.now()
    j = 3
    sum = 0
    while j <= number:
        flag = True
        for each in prime_list:
            if each > math.sqrt(j):
                break
            if j % each == 0:
                flag = False
                break
        if flag:
            prime_list.append(j)
            sum += j

        j += 1

    time2 = datetime.now()

    print(len(prime_list))
    print(time2-time1)
    print(sum)


def prime_sum_2(number):
    time1 = datetime.now()
    is_prime = [0] * number
    i = 3
    sum = 2
    while i <= number:
        if is_prime[i] == 0:
            sum += i
            j = i
            while j < number:
                is_prime[j] = 1
                j += i
        i += 2

    time2 = datetime.now()
    print(time2-time1)
    print(sum)


prime_sum_1(2000000)
prime_sum_2(2000000)
