# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:34:59 2020

@author: Marco
"""
import requests
import re

class Scrapping_dm:
    def __init__(self, headers, seeds):
        self.headers = headers
        self.seeds = seeds
        
    def look_for_links(self):
        links_to_visit = []
        for url in self.seeds:
            req = requests.get(url, headers = self.headers)
            req_text = req.text
            testLINK = re.compile('https://www.dailymail.co.uk/')
            mm = testLINK.finditer(req_text)
            for m in mm:
                link = req_text[m.span()[0]: m.span()[0]+300]
                idx = link.find('"')
                link_clean = link[:idx]
                if link_clean.find('article-') > 0 and link_clean not in self.seeds:
                    links_to_visit.append(link_clean)
        
        links_to_visit = set(links_to_visit)
        links_to_visit = list(links_to_visit)
        return links_to_visit

    
    def grab_summary(self, url):
        req = requests.get(url, headers = self.headers)
        req_text = req.text
        idx = req_text.find('js-article-text')
        end = req_text[idx:].find('</h2>')
        t = req_text[idx + end:] #Empiezo donde termino el titulo
        t2 = t.find('author-section byline-plain')
        t3 = t[:t2] #Texto hasta author
    
        if t3.find('mol-bullets-with-font') == -1:
            text = ''
        else:
            idx = t3.find('mol-bullets-with-font')
            start = t3[idx:].find('>')
            #end = t3[idx:].find('author-section')
            c = t3[idx+start+1:]#idx+end]
            text  = ''
            parag_tag = re.compile('<strong>((.|\n)*?)<\/strong>')
            aa = parag_tag.finditer(c)
            for f in aa:
                text += f.group(1)
                text += '. '
            parag_tag = re.compile('<b>((.|\n)*?)<\/b>')
            aa = parag_tag.finditer(c)
            for f1 in aa:
                text += f1.group(1)
                text += '. '
        summary = text
        return summary
        
    def grab_title(self, url):
        req = requests.get(url, headers = self.headers)
        req_text = req.text
        idx = req_text.find('js-article-text')
        start = req_text[idx:].find('<h2>')
        end = req_text[idx:].find('</h2>')
        title = req_text[idx+start+4:idx+end] 
        return title

       
    def grab_article(self, url):
        req = requests.get(url, headers = self.headers)
        req_text = req.text
        idx = req_text.find('itemprop="articleBody"')
        if req_text[idx:].find('!-- ad') == -1:
            idx_end = req_text[idx:].find('</html>')
        else:    
            idx_end = req_text[idx:].find('!-- ad')
        c = req_text[idx+1:idx+idx_end]
    
        text  = ''
        parag_tag = re.compile('<p((.|\n)*?)<\/p>')
        aa = parag_tag.finditer(c)
        for b in aa:
            text += b.group(0)

        testTAG = re.compile('<.*?>')
        mm = testTAG.finditer(text)
        for m in mm:
            text = text.replace(m.group(0),'')
        text = text.replace('&quot;','')
        text = text.replace('&apos;','')
        text = text.replace('&#39;',"'")
        text = text.replace('Buy now','')
        text = text.replace('\xa0','')
    
        s = text.find('Share what you think')
        if s == -1:
            article = text
        else:
            article = text[:s]
        return article
