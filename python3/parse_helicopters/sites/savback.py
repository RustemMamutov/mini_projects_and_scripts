import requests
from bs4 import BeautifulSoup as bs
import re
import sys
sys.path.append("..")
from sites.constants import URL_LIST
from sites.constants import FIND_ALL_HEL_FUNC
from sites.constants import PARSE_ONE_HEL_FUNC
from sites.constants import HelInfo


def find_all_hel(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    soup = bs(r.text, "html.parser")
    return soup.find_all('div', attrs={"class": re.compile("helicopterBlock id-\w*")})


def parse_one_hel_info(helicopter):
    hell_info = HelInfo()
    hell_info.id = helicopter.attrs["class"][4]
    try:
        hell_info.name = helicopter.find("h3", class_="my-2").string
        hell_info.price = helicopter.find("div", class_="col-md-6").text.strip()
        info = helicopter.find("div", class_="moreInfo").text.replace("\n", "").replace(" ", "")
        info_array = re.split('location|ttaf', info.lower())
        hell_info.year = info_array[0].replace("year", "")
        hell_info.ttaf = info_array[1]
        hell_info.location = info_array[2]
        print()
    except:
        pass

    return hell_info


def get_site_info_dict():
    result = dict()
    result[URL_LIST] = ["https://savback.com/helicopter-inventory/"]
    result[FIND_ALL_HEL_FUNC] = find_all_hel
    result[PARSE_ONE_HEL_FUNC] = parse_one_hel_info
    return result
