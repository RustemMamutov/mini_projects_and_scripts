from result_excel_file import ResultExcelFile
from sites import aircraft24, avbuyer, savback
from sites.constants import *


def init_sites_info_dict():
    result = dict()
    result["avbuyer"] = avbuyer.get_site_info_dict()
    # result["savback"] = savback.get_site_info_dict()
    # result["aircraft24"] = aircraft24.get_site_info_dict()
    return result


sites_info_dict = init_sites_info_dict()


excel_file = ResultExcelFile()
excel_file.ref_create_header_string(1, ["№", "ID", "Name", "Price", "Year", "S/n", "Total time",
                                        "Location", "Info", "Link"])

number = 1
row_number = 2
for site_name, site_info in sites_info_dict.items():
    excel_file.ref_add_data_to_cell(row_number, 1, site_name)
    ur_list = site_info[URL_LIST]
    find_all_hel_func = site_info[FIND_ALL_HEL_FUNC]
    parse_one_hel_func = site_info[PARSE_ONE_HEL_FUNC]
    for each_url in ur_list:
        helicopters = find_all_hel_func(each_url)
        if helicopters is None or len(helicopters) == 0:
            break

        for j in range(0, len(helicopters)):
            current_hel = helicopters[j]
            hell_info = parse_one_hel_func(current_hel)
            hell_info.num = number
            hell_info.print_info()
            row_number += 1
            excel_file.ref_add_data_string(row_number, hell_info)
            number += 1
    row_number += 2

excel_file.workbook.close()
