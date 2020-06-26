# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:34:59 2020

@author: Marco
"""
import requests
import re

class Scrapping_bbc:
    def __init__(self, headers, seeds):
        self.headers = headers
        self.seeds = seeds
        
    def look_for_links(self):
        links_to_visit = []
        for url in self.seeds:
            req = requests.get(url, headers = self.headers)
            req_text = req.text
            testLINK = re.compile('href="')
            mm = testLINK.finditer(req_text)
            for m in mm:
                link = req_text[m.span()[0]+6: m.span()[0]+200]
                idx = link.find('"')
                link_clean = link[:idx]
                if link_clean[-5:].isdigit() and link_clean not in self.seeds:
                    links_to_visit.append(link_clean)
        
        links_to_visit = set(links_to_visit)
        links_to_visit = list(links_to_visit)
        links_to_visit_check = []
        for link in links_to_visit:
            if link[:5] == 'https':
                links_to_visit_check.append(link)
            elif link[:5] == '/news':
                link_cor = 'https://bbc.co.uk' + link
                links_to_visit_check.append(link_cor)
            elif link[:6] == '/sport':
                link_cor = 'https://bbc.co.uk' + link
                links_to_visit_check.append(link_cor)
        return links_to_visit_check
    
    def grab_summary(self, url):
        req = requests.get(url, headers = self.headers)
        req_text = req.text
        idx = req_text.find('story-body__introduction')
        start = req_text[idx:].find('>')
        end = req_text[idx:].find('</p>')
        summary = req_text[idx+start+1:idx+end]
        return summary
       
    def grab_title(self, url):
        req = requests.get(url, headers = self.headers)
        req_text = req.text
        if req_text.find('story-body__h1') == -1:
            idx = req_text.find('story-headline')
        else:
            idx = req_text.find('story-body__h1')
        start = req_text[idx:].find('>')
        end = req_text[idx:].find('</h1>')
        title = req_text[idx+start+1:idx+end] 
        return title
      
    def grab_article(self, url):
        req = requests.get(url, headers = self.headers)
        req_text = req.text
        idx = req_text.find('story-body__introduction')
        start = req_text[idx:].find('</p>') #Starts when the introduction finish
        if req_text[idx:].find('topic-tags') == -1:
            end = req_text[idx:].find('</html>')
        else:
            end = req_text[idx:].find('topic-tags')
        article = req_text[idx+start+1:idx+end]
        
        text  = ''
        parag_tag = re.compile('<p>((.|\n)*?)<\/p>')
        aa = parag_tag.finditer(article)
        for a in aa:
            text += a.group(0)
        
        testTAG = re.compile('<.*?>')
        mm = testTAG.finditer(text)
        for m in mm:
            text = text.replace(m.group(0),'')
        text = text.replace('&quot;','')
        text = text.replace('&apos;','')
        article = text
        return article

