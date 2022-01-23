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
    return soup.find_all('a', attrs={"class": re.compile("ad_listrow")})


def parse_one_hel_info(helicopter):
    hell_info = HelInfo()
    try:
        hell_info.name = helicopter.find("div", class_="ad_listtitle").next
        hell_info.link = 'https://www.aircraft24.com' + helicopter.attrs['href']
        hell_info.price = helicopter.find("span", class_="ad_listprice").text
        info = helicopter.find("div", class_="ad_listpriceadditions").nextSibling.lower()
        info_array = info.split(";")
        year = None
        ttaf = None
        location = None
        for each in info_array:
            if "year" in each:
                year = each
                continue
            if "ttaf" in each:
                ttaf = each
                continue
            if "location" in each:
                location = each
                continue
        if year is not None:
            hell_info.year = year.replace("year", "").replace(":", "").replace(" ", "")
        if ttaf is not None:
            hell_info.ttaf = ttaf.replace("ttaf", "").replace(":", "").replace(" ", "")
        if location is not None:
            hell_info.location = location.replace("location", "").replace(":", "").replace(" ", "")
    except:
        pass

    return hell_info


def get_site_info_dict():
    result = dict()
    url_list = list()
    for i in range(1, 2):
        url_list.append("https://www.aircraft24.com/search/search-helicopter.htm?dosearch=1&SEARCH_ADTYPE_ID=H&showpage={}".format(i))

    result[URL_LIST] = url_list
    result[FIND_ALL_HEL_FUNC] = find_all_hel
    result[PARSE_ONE_HEL_FUNC] = parse_one_hel_info
    return result
