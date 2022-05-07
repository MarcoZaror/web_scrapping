# -*- coding: utf-8 -*-

import argparse
import logging

from tqdm import tqdm

from Data import DataManager
from seeds import BBC, DM
from web_scrapping import WebScrapperBBC, WebScrapperDM

logger = logging.getLogger("webScrapper")


def main(news_provider: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if news_provider == "BBC":
        seeds = BBC
        web_scrapper = WebScrapperBBC(headers, seeds)
    elif news_provider == "DM":
        seeds = DM
        web_scrapper = WebScrapperDM(headers, seeds)
    else:
        logger.error("News provider must be either BBC or DM")

    data_manager = DataManager(news_provider)
    content = data_manager.load_content()
    key = len(content) + 1
    new_content = {}

    links = web_scrapper.look_for_links()
    for link in tqdm(links):
        summary = web_scrapper.grab_summary(link)
        title = web_scrapper.grab_title(link)
        article = web_scrapper.grab_article(link)
        new_content[key] = {}
        new_content[key]["link"] = link
        new_content[key]["summary"] = summary
        new_content[key]["title"] = title
        new_content[key]["article"] = article
        key += 1

    data_manager.update_content(new_content)
    data_manager.remove_duplicates()
    data_manager.write_content()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--news_provider",
        type=str,
        default="BBC",
        help="News provider to get news from.",
    )
    args = parser.parse_args()
    main(args.news_provider)
