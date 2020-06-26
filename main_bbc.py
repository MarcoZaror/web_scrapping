# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:35:50 2020

@author: Marco
"""
from Data import Data
from Scrapping_bbc import Scrapping_bbc

def main():
    #Need to create a dictionary at the beginning (just for the first time)
    path = 'C:/Users/Marco/Documents/MSc/Tesis/content_bbc.json'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    seeds =[
    'https://www.bbc.co.uk/news/uk',
    'https://www.bbc.co.uk/news/england',
    'https://www.bbc.co.uk/news/northern_ireland',
    'https://www.bbc.co.uk/news/scotland',
    'https://www.bbc.co.uk/news/wales',
    'https://www.bbc.co.uk/news/localnews',
    'https://www.bbc.co.uk/news/world',
    'https://www.bbc.co.uk/news/world/africa',
    'https://www.bbc.co.uk/news/world/asia',
    'https://www.bbc.co.uk/news/world/australia',
    'https://www.bbc.co.uk/news/world/europe',
    'https://www.bbc.co.uk/news/world/latin_america',
    'https://www.bbc.co.uk/news/world/middle_east',
    'https://www.bbc.co.uk/news/world/us_and_canada',
    'https://www.bbc.co.uk/news/business',
    'https://www.bbc.co.uk/news/business/your_money',
    'https://www.bbc.co.uk/news/business/market-data',
    'https://www.bbc.co.uk/news/business/companies',
    'https://www.bbc.co.uk/news/business/economy',
    'https://www.bbc.co.uk/news/business/global_car_industry',
    'https://www.bbc.co.uk/news/business/business_of_sport',
    'https://www.bbc.co.uk/news/politics',
    'https://www.bbc.co.uk/news/politics/parliaments',
    'https://www.bbc.co.uk/news/politics/uk_leaves_the_eu',
    'https://www.bbc.co.uk/news/election/2019',
    'https://www.bbc.co.uk/news/technology',
    'https://www.bbc.co.uk/news/science_and_environment',
    'https://www.bbc.co.uk/news/health',
    'https://www.bbc.co.uk/news/education',
    'https://www.bbc.co.uk/news/entertainment_and_arts',
    'https://www.bbc.co.uk/news/stories',
    'https://www.bbc.co.uk/news/newsbeat',
    'https://www.bbc.co.uk/sport',
    'https://www.bbc.co.uk/sport/football',
    'https://www.bbc.co.uk/sport/formula1',
    'https://www.bbc.co.uk/sport/cricket',
    'https://www.bbc.co.uk/sport/rugby_union',
    'https://www.bbc.co.uk/sport/rugby_league',
    'https://www.bbc.co.uk/sport/tennis',
    'https://www.bbc.co.uk/sport/golf',
    'https://www.bbc.co.uk/sport/athletics',
    ]
    ct = Data()
    ctnt = ct.load_content(path)
    key = len(ctnt) + 1
    ctnt_new = {}
    
    sc = Scrapping_bbc(headers, seeds)
    links = sc.look_for_links()
    for link in links:
        summary = sc.grab_summary(link)
        title = sc.grab_title(link)
        article = sc.grab_article(link)
        ctnt_new[key] = {}
        ctnt_new[key]['link'] = link
        ctnt_new[key]['summary'] = summary
        ctnt_new[key]['title'] = title
        ctnt_new[key]['article'] = article
        key += 1
    content2 = {}
    for c in ctnt_new:
        if ctnt_new[c]['article'] == '' or ctnt_new[c]['title'] == '' or \
        ctnt_new[c]['summary'] == '' or ctnt_new[c]['link'] == '':
            pass
        else:
            content2[c] = ctnt_new[c]
    
    ct.update_content(content2)
    ct.remove_dup()
    ct.write_content(path)
        
if __name__ == '__main__':
    main()