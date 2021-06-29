#!/usr/bin/env python3

# This script will output a spreadsheet of the frequency rank of every species found in every county
# final spreadsheet will have counties as entries/rows and species as fields/columns

from ast import literal_eval
import requests
from bs4 import BeautifulSoup
from time import sleep
import json

key = 'XXXXXXXXXXX'  # eBird API key goes here
session = 'XXXXXXXXXXXXXXXXXXX'  # ebird.org session cookie goes here
headers = {"X-eBirdApiToken": key}
cookies = {"EBIRD_SESSIONID": session}


def main():
    # get list of all counties
    response = requests.get("https://api.ebird.org/v2/ref/region/list/subnational2/US", headers=headers)
    all_counties = literal_eval(response.text)
    del response
    # all_counties = [{"code": "US-NC-113", "name": "Macon"},
    #                 {"code": "US-CO-107", "name": "Routt"},
    #                 {"code": "US-IL-187", "name": "Warren"}]

    # sort by region code
    all_counties.sort(key=lambda item: item.get("code"))
    # print(all_counties)

    for county in all_counties:
        # get target page
        response = requests.get("https://ebird.org/targets?r1={0}&r2=AQ".format(county["code"]), cookies=cookies)

        # scrape the page for the species and ranks
        soup = BeautifulSoup(response.text, 'html.parser')

        # for every div class="ResultsStats ResultsStats--action ResultsStats--toEdge"
        for div1 in soup.find_all("div", class_="ResultsStats ResultsStats--action ResultsStats--toEdge"):
            # rank = content of > div class="ResultsStats-index"
            rank = div1.get_text().split()[0][:-1]
            # species = content of tag data-species-code of > div class=ResultsStats-title > div > h5 > a
            species = div1.find(attrs={"data-species-code": True})['data-species-code']
            # frequency =  content of title tag of > div class ResultsStats-stats
            freq = div1.find(class_="ResultsStats-stats")['title'][:-11]

            county.update({species: {"rank": rank, "frequency": freq}})

        print(county["code"] + " " + county["name"])  # where we at
        sleep(1)  # rate limit
        break  # uncomment to only run on the first county

    if usefile:
        with open('output.txt', 'w+') as file:
            file.write(str(all_counties))
    else:
        # create and save spreadsheet
        # possibly in a separate script and possibly using google sheets api
        pass


if __name__ == "__main__":
    usefile = 1  # 0: write spreadsheet  1: write dict to file  2: read from old file
    main()
    if usefile == 2:
        with open('output.txt', 'r') as file:
            data = file.read()
        # data = literal_eval(data)
        print(data[:50])
        data = json.loads(data[1:-1])
        print(type(data))
