summ_of_squares = 0
square_of_summ = 0
i = 1
while i <= 100:
    summ_of_squares += i*i
    square_of_summ += i
    i += 1
square_of_summ *= square_of_summ
print(square_of_summ - summ_of_squares)