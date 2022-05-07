import logging
import re
from typing import List, Set

import requests

logger = logging.getLogger("webScrapper")


def get_url_content(url, headers):
    # TODO - cache results
    return requests.get(url, headers=headers)


class WebScrapperBBC:
    # TODO - create abstract class
    def __init__(self, headers, seeds):
        self.headers = headers
        self.seeds = seeds

    def look_for_links(self) -> List:
        logger.info("Looking for links")
        links_to_visit = []
        for url in self.seeds:
            req = requests.get(url, headers=self.headers)
            links_text = re.compile('href="')
            links = links_text.finditer(req.text)
            for link in links:
                link = req.text[link.span()[0] + 6: link.span()[0] + 200]
                idx = link.find('"')
                link_clean = link[:idx]
                if link_clean[-5:].isdigit() and link_clean not in self.seeds:
                    links_to_visit.append(link_clean)

        links_to_visit = set(links_to_visit)
        links_to_visit_checked = []
        for link in links_to_visit:
            if link[:5] == "https":
                links_to_visit_checked.append(link)
            elif link[:5] == "/news":
                corrected_link = "https://bbc.co.uk" + link
                links_to_visit_checked.append(corrected_link)
            elif link[:6] == "/sport":
                corrected_link = "https://bbc.co.uk" + link
                links_to_visit_checked.append(corrected_link)
        return links_to_visit_checked

    def grab_summary(self, url: str) -> str:
        logger.info("Grabbing summary")
        req = get_url_content(url, self.headers)
        idx = req.text.find("story-body__introduction")
        start = req.text[idx:].find(">")
        end = req.text[idx:].find("</p>")
        summary = req.text[idx + start + 1 : idx + end]
        return summary

    def grab_title(self, url: str) -> str:
        logger.info("Grabbing title")
        req = get_url_content(url, self.headers)
        if req.text.find("story-body__h1") == -1:
            idx = req.text.find("story-headline")
        else:
            idx = req.text.find("story-body__h1")
        start = req.text[idx:].find(">")
        end = req.text[idx:].find("</h1>")
        title = req.text[idx + start + 1 : idx + end]
        return title

    def grab_article(self, url: str) -> str:
        logger.info("Grabbing article")
        req = get_url_content(url, self.headers)
        idx = req.text.find("story-body__introduction")
        start = req.text[idx:].find("</p>")
        if req.text[idx:].find("topic-tags") == -1:
            end = req.text[idx:].find("</html>")
        else:
            end = req.text[idx:].find("topic-tags")
        article = req.text[idx + start + 1 : idx + end]

        text = ""
        parag_tag = re.compile("<p>((.|\n)*?)<\/p>")
        paragraphs = parag_tag.finditer(article)
        for paragraph in paragraphs:
            text += paragraph.group(0)

        tag_text = re.compile("<.*?>")
        tags = tag_text.finditer(text)
        for tag in tags:
            text = text.replace(tag.group(0), "")
        text = text.replace("&quot;", "")
        text = text.replace("&apos;", "")
        article = text
        return article


class WebScrapperDM:
    # TODO - create abstract class
    def __init__(self, headers, seeds):
        self.headers = headers
        self.seeds = seeds

    def look_for_links(self) -> Set:
        logger.info("Looking for links")
        links_to_visit = []
        for url in self.seeds:
            req = requests.get(url, headers=self.headers)
            req_text = req.text
            links_text = re.compile("https://www.dailymail.co.uk/")
            links = links_text.finditer(req_text)
            for link in links:
                link = req_text[link.span()[0] : link.span()[0] + 300]
                idx = link.find('"')
                link_clean = link[:idx]
                if link_clean.find("article-") > 0 and link_clean not in self.seeds:
                    links_to_visit.append(link_clean)

        links_to_visit = set(links_to_visit)
        return links_to_visit

    def grab_summary(self, url: str) -> str:
        logger.info("Grabbing summary")
        req = get_url_content(url, self.headers)
        idx = req.text.find("js-article-text")
        end = req.text[idx:].find("</h2>")
        t = req.text[idx + end :]
        t2 = t.find("author-section byline-plain")
        t3 = t[:t2]

        if t3.find("mol-bullets-with-font") == -1:
            text = ""
        else:
            idx = t3.find("mol-bullets-with-font")
            start = t3[idx:].find(">")
            c = t3[idx + start + 1 :]
            text = ""
            parag_tag = re.compile("<strong>((.|\n)*?)<\/strong>")
            paragraphs = parag_tag.finditer(c)
            for paragraph in paragraphs:
                text += paragraph.group(1)
                text += ". "
            parag_tag = re.compile("<b>((.|\n)*?)<\/b>")
            paragraphs = parag_tag.finditer(c)
            for paragraph in paragraphs:
                text += paragraph.group(1)
                text += ". "
        summary = text
        return summary

    def grab_title(self, url: str) -> str:
        logger.info("Grabbing title")
        req = get_url_content(url, self.headers)
        idx = req.text.find("js-article-text")
        start = req.text[idx:].find("<h2>")
        end = req.text[idx:].find("</h2>")
        title = req.text[idx + start + 4 : idx + end]
        return title

    def grab_article(self, url: str) -> str:
        logger.info("Grabbing article")
        req = get_url_content(url, self.headers)
        idx = req.text.find('itemprop="articleBody"')
        if req.text[idx:].find("!-- ad") == -1:
            idx_end = req.text[idx:].find("</html>")
        else:
            idx_end = req.text[idx:].find("!-- ad")
        relevant_text = req.text[idx + 1 : idx + idx_end]

        text = ""
        parag_tag = re.compile("<p((.|\n)*?)<\/p>")
        aa = parag_tag.finditer(relevant_text)
        for b in aa:
            text += b.group(0)

        tags_text = re.compile("<.*?>")
        tags = tags_text.finditer(text)
        for tag in tags:
            text = text.replace(tag.group(0), "")
        text = text.replace("&quot;", "")
        text = text.replace("&apos;", "")
        text = text.replace("&#39;", "'")
        text = text.replace("Buy now", "")
        text = text.replace("\xa0", "")

        s = text.find("Share what you think")
        if s == -1:
            article = text
        else:
            article = text[:s]
        return article
