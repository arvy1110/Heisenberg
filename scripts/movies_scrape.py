# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 23:10:07 2019

@author: arvys
"""

import wikipedia
import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# first pull the HTML from the page that links to all of the pages with the links.
# in this case, this page gives the links list pages of sci-fi films by decade.
# just go to https://en.wikipedia.org/wiki/Lists_of_science_fiction_films
# to see what I'm pulling from.
html = requests.get('https://en.wikipedia.org/wiki/Lists_of_Bollywood_films')
html = requests.get('https://en.wikipedia.org/wiki/Lists_of_science_fiction_films')

#turn the HTML into a beautiful soup text object
b = BeautifulSoup(html.text, 'lxml')
#print (b)
# create an mpty list where those links will go.
links = []

# in this case, all of the links we're in a '<li>' brackets.
for i in b.find_all(name = 'li'):
    # pull the actual link for each one
    for link in i.find_all('a', href=True):
        links.append(link['href'])
# the above code ends up pulling more links than I want,
# so I just use the ones I want
links = links[13]
print (links)
# each link only returns something like 'wiki/List_of_science_fiction_films_of_the_1920s'
# so I add the other part of the URL to each.
decade_links = ['https://en.wikipedia.org' + links]
print (decade_links)

# create two new lists, one for the title of the page, 
# and one for the link to the page
film_titles = []
film_links = []
film_genre = []
# for loop to pull from each decade page with list of films.
# look at https://en.wikipedia.org/wiki/List_of_science_fiction_films_of_the_1920s
# to follow along as an exampe
for decade in decade_links:
    print(f'Collecting films from {decade}')
    html = requests.get(decade)
    b = BeautifulSoup(html.text, 'lxml')
    print (b)
    # get to the table on the page
    for i in b.find_all(name='table', class_='wikitable'):
        # get to the row of each film
        for j in i.find_all(name='tr'):
            #get just the title cell for each row.
            # contains the title and the URL
            for k in j.find_all(name='i'):
                # get within that cell to just get the words
                for link in k.find_all('a', href=True):
                    # get the title and add to the list
                    film_titles.append(link['title'])
                    # get the link and add to that list
                    film_links.append(link['href'])
    #be a conscientious scraper and pause between scrapes
    time.sleep(1)
print(f'Number of Film Links Collected: {len(film_links)}')
print(f'Number of Film Titles Collected: {len(film_titles)}')
print(film_titles)
# remove film links that don't have a description page on Wikipedia
new_film_links = [i for i in film_links if 'redlink' not in i]
# same goes for titles
new_film_titles = [i for i in film_titles if '(page does not exist)' not in i]
print(f'Number of Film Links with Wikipedia Pages: {len(new_film_links)}')
print(f'Number of Film Titles with Wikipedia Pages: {len(new_film_titles)}')
#use this list to fetch from the API
title_links = list(zip(new_film_titles, new_film_links))