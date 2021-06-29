#!/usr/bin/python3

import requests
import json
from bs4 import BeautifulSoup
from time import sleep



url = "https://ebird.org/targets?r2=AQ&r1="
cookies = {'EBIRD_SESSIONID': 'F4BA26BD1675CFC151862954CA1758C2'}

final_sp = set()


def main():
    global final_sp

    # parse county list from file

    with open('counties.json') as open_file:
        data = json.load(open_file)

    # counter = 0
    for county in data:
        # counter += 1
        
        county.update({'sp': {}})
        
        response = requests.get(f'{url}{county["code"]}', cookies=cookies)
        # parse page

        # scrape the page for the species and ranks
        soup = BeautifulSoup(response.text, 'html.parser')

        # for every div class="ResultsStats ResultsStats--action ResultsStats--toEdge"
        for div1 in soup.find_all("div", class_="ResultsStats ResultsStats--action ResultsStats--toEdge"):
            # rank = content of > div class="ResultsStats-index"
            rank = div1.get_text().split()[0][:-1]
            # species = content of tag data-species-code of > div class=ResultsStats-title > div > h5 > a
            species = div1.find(attrs={"data-species-code": True})['data-species-code']
            final_sp.add(species)
            # frequency =  content of title tag of > div class ResultsStats-stats
            freq = div1.find(class_="ResultsStats-stats")['title'][:-11]

            county['sp'].update({species: {"rank": rank, "frequency": freq}})

        print(county["code"] + " " + county["name"])  # where we at
        
        
        # if counter > 3:
        #     break
        
        sleep(1)  # rate limit
    
    final_sp = list(final_sp)  # lock species list in to final order
    
    return data


def create_file(data):
    """
    Write values to final output file.
    """
    global final_sp
    final = ",Species:,"
    
    print('Adding species to file contents...')
    
    for sp in final_sp:
        final += f'{sp},'
    final += '\n'
    
    print('Adding counties to file contents...')
    
    c = ','
    
    for county in data:
        final += f'{county["code"]},{county["name"] + " " + county["code"][3:5]}'
        
        # construct string containing species ranks
        
        sp_str = c * len(final_sp)
        
        for sp in county['sp']:
            # get current comma positions
            positions = [pos for pos, char in enumerate(sp_str) if char == c]
            # print(positions)
            # print(final_sp)
            
            # get position of sp in final_sp
            p = final_sp.index(sp)
            p1 = positions[p] + 1
            
            # write sp['rank'] to correct position
            sp_str = sp_str[:p1] + county['sp'][sp]['rank'] + sp_str[p1:]

        final += sp_str
        
        final += '\n'
    
    
    print('Writing file...')
    with open('counties_spreadsheet.csv', 'w+') as open_file:
        open_file.write(final)
    
    
    # print(final)


if __name__ == "__main__":
    data = main()
    
    create_file(data)
    
