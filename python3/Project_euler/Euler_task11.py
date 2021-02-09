grid = \
    [
        "0802229738150040007504050778521250779108",
        "4949994017811857608717409843694804566200",
        "8149317355791429937140675388300349133665",
        "5270952304601142692468560132567137023691",
        "2231167151676389419236542240402866331380",
        "2447326099034502447533537836842035171250",
        "3298812864236710263840675954706618386470",
        "6726206802621220956394396308409166499421",
        "2455580566739926971778789683148834896372",
        "2136230975007644204535140061339734313395",
        "7817532822753167159403800462161409535692",
        "1639054296353147555888240017542436298557",
        "8656004835718907054444374460215851541758",
        "1980816805944769287392138652177704895540",
        "0452088397359916079757321626267933279866",
        "8836688757622072034633674655123263935369",
        "0442167338253911249472180846293240627636",
        "2069364172302388346299698267598574043616",
        "2073352978319001743149714886811623570554",
        "0170547183515469169233486143520189196748"
     ]

grid1 = list()

for each in grid:
    local_list = list()
    length = int(len(each)/2)
    for i in range(0, length):
        local_list.append(each[(2 * i):(2 * i + 2)])
    print(local_list)
    grid1.append(local_list)

maximum = 0


def mulriply_and_print(a, b, c, d, max_to_compare):
    local_result = a * b * c * d
    print("{}-{}: {}_{}_{}_{}"
          .format(i, j, a, b, c, d))
    print(local_result)

    if local_result > max_to_compare:
        max_to_compare = local_result
        print("========= " + str(max_to_compare))
    return max_to_compare


def calculate_diag1(i, j, max):
    a = int(grid1[i][j])
    b = int(grid1[i + 1][j + 1])
    c = int(grid1[i + 2][j + 2])
    d = int(grid1[i + 3][j + 3])
    return mulriply_and_print(a, b, c, d, max)


def calculate_diag2(i, j, max):
    a = int(grid1[i][j])
    b = int(grid1[i + 1][j - 1])
    c = int(grid1[i + 2][j - 2])
    d = int(grid1[i + 3][j - 3])
    return mulriply_and_print(a, b, c, d, max)


def calculate_horiz(i, j, max):
    a = int(grid1[i][j])
    b = int(grid1[i][j + 1])
    c = int(grid1[i][j + 2])
    d = int(grid1[i][j + 3])
    return mulriply_and_print(a, b, c, d, max)


def calculate_vertik(i, j, max):
    a = int(grid1[i][j])
    b = int(grid1[i+1][j])
    c = int(grid1[i+2][j])
    d = int(grid1[i+3][j])
    return mulriply_and_print(a, b, c, d, max)


for i in range(0, 17):
    for j in range(0, 17):
        print("diagonal")
        maximum = calculate_diag1(i, j, maximum)
        print("horizontal")
        maximum = calculate_horiz(i, j, maximum)
        print("vertical")
        maximum = calculate_vertik(i, j, maximum)


for i in range(0, 17):
    for j in range(3, 20):
        print("diagonal")
        maximum = calculate_diag2(i, j, maximum)


print(maximum)
