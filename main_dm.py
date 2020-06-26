# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:35:50 2020

@author: Marco
"""
from Data import Data
from Scrapping_dm import Scrapping_dm

def main():
    #Need to create a dictionary at the beginning (just for the first time)
    path = 'C:/Users/Marco/Documents/MSc/Tesis/content_dm.json'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    seeds =[
'https://www.dailymail.co.uk/home/index.html',
'https://www.dailymail.co.uk/home/latest/index.html',
'https://www.dailymail.co.uk/news/worldnews/index.html',
'https://www.dailymail.co.uk/home/you/index.html',
'https://www.dailymail.co.uk/home/event/index.html',
'https://www.dailymail.co.uk/home/books/index.html',
'https://www.dailymail.co.uk/property/index.html',
'https://www.dailymail.co.uk/motoring/index.html',
'https://www.dailymail.co.uk/columnists/index.html',
'https://www.dailymail.co.uk/news/coronavirus/index.html',
'https://www.dailymail.co.uk/news/royal/index.html',
'https://www.dailymail.co.uk/news/prince-andrew/index.html',
'https://www.dailymail.co.uk/news/arts/index.html',
'https://www.dailymail.co.uk/news/headlines/index.html',
'https://www.dailymail.co.uk/news/france/index.html',
'https://www.dailymail.co.uk/news/mostread/index.html',
'https://www.dailymail.co.uk/wires/index.html',
'https://www.dailymail.co.uk/sport/index.html',
'https://www.dailymail.co.uk/sport/football/index.html',
'https://www.dailymail.co.uk/sport/premierleague/index.html',
'https://www.dailymail.co.uk/sport/champions_league/index.html',
'https://www.dailymail.co.uk/sport/transfernews/index.html',
'https://www.dailymail.co.uk/sport/boxing/index.html',
'https://www.dailymail.co.uk/sport/rugbyunion/index.html',
'https://www.dailymail.co.uk/sport/golf/index.html',
'https://www.dailymail.co.uk/sport/cricket/index.html',
'https://www.dailymail.co.uk/sport/formulaone/index.html',
'https://www.dailymail.co.uk/sport/tennis/index.html',
'https://www.dailymail.co.uk/sport/racing/index.html',
'https://www.dailymail.co.uk/sport/othersports/index.html',
'https://www.dailymail.co.uk/sport/mma/index.html',
'https://www.dailymail.co.uk/usshowbiz/index.html',
'https://www.dailymail.co.uk/tvshowbiz/headlines/index.html',
'https://www.dailymail.co.uk/tvshowbiz/oscars/index.html',
'https://www.dailymail.co.uk/tvshowbiz/love-island/index.html',
'https://www.dailymail.co.uk/news/breaking_news/index.html',
'https://www.dailymail.co.uk/news/sydney/index.html',
'https://www.dailymail.co.uk/news/melbourne/index.html',
'https://www.dailymail.co.uk/news/brisbane/index.html',
'https://www.dailymail.co.uk/news/perth/index.html',
'https://www.dailymail.co.uk/news/adelaide/index.html',
'https://www.dailymail.co.uk/news/new_zealand/index.html',
'https://www.dailymail.co.uk/news/australia-fires/index.html',
'https://www.dailymail.co.uk/tvshowbiz/meghan-markle/index.html',
'https://www.dailymail.co.uk/femail/food/index.html',
'https://www.dailymail.co.uk/home/gardening/index.html',
'https://www.dailymail.co.uk/health/index.html',
'https://www.dailymail.co.uk/sciencetech/index.html',
'https://www.dailymail.co.uk/money/index.html',
'https://www.dailymail.co.uk/money/markets/index.html',
'https://www.dailymail.co.uk/money/saving/index.html',
'https://www.dailymail.co.uk/money/investing/index.html',
'https://www.dailymail.co.uk/money/bills/index.html',
'https://www.dailymail.co.uk/money/cars/index.html',
'https://www.dailymail.co.uk/money/holidays/index.html',
'https://www.dailymail.co.uk/money/pensions/index.html',
'https://www.dailymail.co.uk/money/mortgageshome/index.html',
'https://www.dailymail.co.uk/money/cardsloans/index.html'
]
    ct = Data()
    ctnt = ct.load_content(path)
    key = len(ctnt) + 1
    ctnt_new = {}
    
    sc = Scrapping_dm(headers, seeds)
    links = sc.look_for_links()
    for link in links:
        #print(link)
        summary = sc.grab_summary(link)
        title = sc.grab_title(link)
        article = sc.grab_article(link)
        ctnt_new[key] = {}
        ctnt_new[key]['link'] = link
        ctnt_new[key]['summary'] = summary
        ctnt_new[key]['title'] = title
        ctnt_new[key]['article'] = article
        key += 1
    ct.update_content(ctnt_new)
    ct.remove_dup()
    ct.write_content(path)
        
if __name__ == '__main__':
    main()