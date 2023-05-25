import os

global_path = os.getcwd().replace("\\", "/")

SIZE_10GB = (10 * 1024 * 1024 * 1024) - 1
SIZE_1GB = (1024 * 1024 * 1024) - 1
SIZE_500MB = (1024 * 1024) * 500 - 1
SIZE_200MB = (1024 * 1024) * 200 - 1
SIZE_100MB = (1024 * 1024) * 100 - 1
SIZE_50MB = (1024 * 1024) * 50 - 1
SIZE_20MB = (1024 * 1024) * 20 - 1
SIZE_10MB = (1024 * 1024) * 10 - 1
SIZE_5MB = (1024 * 1024) * 5 - 1
SIZE_2MB = (1024 * 1024) * 2 - 1
SIZE_1MB = (1024 * 1024) - 1
SIZE_500KB = 1024 * 500 - 1
SIZE_200KB = 1024 * 200 - 1
SIZE_100KB = 1024 * 100 - 1
SIZE_50KB = 1024 * 50 - 1
SIZE_20KB = 1024 * 20 - 1
SIZE_10KB = 1024 * 10 - 1
SIZE_5KB = 1024 * 5 - 1
SIZE_2KB = 1024 * 2 - 1
SIZE_1KB = 1024


def create_file(name, size):
    file_full_path = "{0}/{1}".format(global_path, name)
    with open(file_full_path, "wb") as out:
        out.write(bytes("1", 'utf-8'))
        out.seek(size)
        out.write(bytes("1", 'utf-8'))

# create_file("01_1KB.txt", SIZE_1KB)
# create_file("02_2KB.txt", SIZE_2KB)
# create_file("03_5KB.txt", SIZE_5KB)
# create_file("04_10KB.txt", SIZE_10KB)
# create_file("05_20KB.txt", SIZE_20KB)
# create_file("06_50KB.txt", SIZE_50KB)
# create_file("07_100KB.txt", SIZE_100KB)
# create_file("08_200KB.txt", SIZE_200KB)
# create_file("09_500KB.txt", SIZE_500KB)
# create_file("10_1MB.txt", SIZE_1MB)
# create_file("11_2MB.txt", SIZE_2MB)
# create_file("12_5MB.txt", SIZE_5MB)
# create_file("13_10MB.txt", SIZE_10MB)
# create_file("14_20MB.txt", SIZE_20MB)
# create_file("15_50MB.txt", SIZE_50MB)
# create_file("16_100MB.txt", SIZE_100MB)
# create_file("17_200MB.txt", SIZE_200MB)
# create_file("18_500MB.txt", SIZE_500MB)
# create_file("19_1GB.txt", SIZE_1GB)
# create_file("20_10GB.txt", SIZE_10GB)

SIZE_GB = 1.0

create_file("test.txt", (int (SIZE_GB * 1024 * 1024 * 1024)) - 1)



