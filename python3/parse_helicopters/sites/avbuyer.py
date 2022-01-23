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
    return soup.find_all('div', attrs={"id": re.compile("item_card_\w*")})


def parse_one_hel_info(helicopter):
    hell_info = HelInfo()
    hell_info.site_name = "avbyer"
    hell_info.id = helicopter.attrs["id"].split("_")[2]
    try:
        content = helicopter \
            .find("div", class_="grid-x list-content") \
            .find("div", class_="auto cell") \
            .find("div", class_="list-item-details")
        hell_info.name = content.find("h2", class_="item-title").text.strip()
        hell_info.link = content.find("h2", class_="item-title").contents[0]
        price = content.find("div", class_="price").text.lower()
        if "price" in price:
            price = price.replace(" ", "").replace("price", " ").strip().split(" ")[0].replace(":", "")
        hell_info.price = price
        info = content\
            .find("div", class_="list-other-dtl")\
            .find("ul", class_="fa-no-bullet clearfix")\
            .text.replace(" ", "")
        info_array = re.split('totaltime|s/n', info.lower())
        hell_info.year = info_array[0].replace("year", "")
        hell_info.serial_num = info_array[1]
        hell_info.ttaf = info_array[2]
    except:
        pass

    return hell_info


def get_site_info_dict():
    result = dict()
    url_list = list()
    for i in range(1, 100):
        url_list.append("https://www.avbuyer.com/aircraft/helicopter/turbine/page-{}".format(i))

    result[URL_LIST] = url_list
    result[FIND_ALL_HEL_FUNC] = find_all_hel
    result[PARSE_ONE_HEL_FUNC] = parse_one_hel_info
    return result
