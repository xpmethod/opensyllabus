#!/usr/bin/python
from bs4 import BeautifulSoup
import re

def soupify(html_file):
    return BeautifulSoup(html_file)
    
def pretty_print(soup):    
    print(soup.prettify())
    
def find_attribute(soup, attr, search_str):
    return soup.find_all(attrs = {attr : re.compile(search_str)})

if __name__ == '__main__':
    with open('../output/Leonard_Women_Music_syllabus.html') as file:
        soup = soupify(file)
        pretty_print(soup)
        elements = find_attribute(soup, 'style', r'Bold')
        for element in elements:
            print element