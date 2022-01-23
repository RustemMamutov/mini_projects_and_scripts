URL_LIST = "ur_list"
FIND_ALL_HEL_FUNC = "find_all_hel_func"
PARSE_ONE_HEL_FUNC = "parse_one_hel_func"
NO_DATA = "--"


class HelInfo:
    def __init__(self):
        self.num = NO_DATA
        self.id = NO_DATA
        self.name = NO_DATA
        self.price = NO_DATA
        self.year = NO_DATA
        self.serial_num = NO_DATA
        self.ttaf = NO_DATA
        self.location = NO_DATA
        self.info = NO_DATA
        self.link = NO_DATA

    def print_info(self):
        print("№{} __ {} __ {} __ {} __ {} __ {} __ {} __ {} __ {} __ {}".format(
            self.num, self.id, self.name, self.price, self.year, self.serial_num,
            self.ttaf, self.location, self.info, self.link))
