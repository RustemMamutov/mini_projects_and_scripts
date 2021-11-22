import gzip
from random import randrange
import tarfile
import os

total_files_count = 30


def compress(output_file, output_dir, root_dir, items):
    """compress dirs.

    KWArgs
    ------
    output_file : str, default ="archive.tar.gz"
    output_dir : str, default = ''
        absolute path to output
    root_dir='.',
        absolute path to input root dir
    items : list
        list of dirs/items relative to root dir

    """
    os.chdir(root_dir)
    with tarfile.open(os.path.join(output_dir, output_file), "w:gz") as tar:
        for item in items:
            tar.add(item, arcname=item)    


content_dict = dict()

for i in range(0, total_files_count):
    content = ""
    for j in range (0, 10):
        content += "rustem" + str(randrange(1000)) + "\n"
    content_dict[i] = content

gz_name_list = list()

for each_key in content_dict.keys():
    filename = "gz_archive_" + str(each_key+1) + ".gz"
    filepath = "C:/Users/Rustem/Desktop/test/" + filename
    gz_name_list.append(filename)
    print("content: " + content_dict[each_key])
    content_as_byte_array = bytearray()
    content_as_byte_array.extend(map(ord, content_dict[each_key]))
    with gzip.open(filename, 'wb') as f:
        f.write(content_as_byte_array)
        
for i in range(0, int(total_files_count/10)):
    items_to_tar = list()
    for j in range(0, 10):
        items_to_tar.append(gz_name_list[i*10 + j])
    tar_gz_filename = "C:/Users/Rustem/Desktop/test/tar_gz_archive_" + str(i+1) + ".tar.gz"
    compress(tar_gz_filename, "", "..", items_to_tar)
