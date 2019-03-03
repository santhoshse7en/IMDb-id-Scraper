# Import Packages
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import argparse
import time
import sys
import re

# Retrieve IMDb person/company/title id
def IMDbID(argv):
    """
    'IMDbID' method takes a person/company/title name, searches for the similar person/company/title names available in IMDb.
    and suggests the person/company/title name to the user. Based upon user's selection it returns a list of person/company/title ids.

    Input serial numbers separated with spaces.

    -------------------- -------------------- -------------------- -------------------- --------------------
    :param movie: Person Name/ Company Name / Title Name.
    :returns: A list of person/company/title ids.
    :raises ValueError: Raises an exception when entered a charater other than a number for selection.
    :raises IndexError: Raises an BeautifulSoup exception when index is out of range.
    """

    parser = argparse.ArgumentParser(add_help=False, description=('Download Youtube comments without using the Youtube API'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    parser.add_argument('--name', '-n', help='Enter the name of which to extract IMDb id')
    args = parser.parse_args(argv)

    suggestions, imdbids = [], []
    url = 'https://www.imdb.com/find?ref_=nv_sr_fn&q=' + ''.join(args.name.split()) + '&s=all'
    response = get(url)
    soup_obj = BeautifulSoup(response.text, 'lxml')
    try:
        if len(soup_obj.select('.result_text')) > 20:
            for item in soup_obj.select('.result_text')[:20]:
                print('%s' %(soup_obj.select('.result_text').index(item) + 1) + ': ' + item.text.strip())
                suggestions.append(item.a['href'].split('/')[2].strip())
        else:
            for item in soup_obj.select('.result_text'):
                print('%s' %(soup_obj.select('.result_text').index(item) + 1) + ': ' + item.text.strip())
                suggestions.append(item.a['href'].split('/')[2].strip())
        imdbids = [ suggestions[int(load) - 1] if int(load) != 0 else '' for load in re.findall(r"[\w']+", input('\nEnter serial number\t')) ]
        if len(imdbids) == 1:
            return imdbids[0]
        else:
            return imdbids
    except Exception as es:
        print("{0} :".format(type(es)), es)
        sys.exit(0)

if __name__ == '__main__':
    try:
        identifer = IMDbID(sys.argv[1:])
        print("\nIMDb id : ", identifer)
    except:
        print('Inappropriate input')
