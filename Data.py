# -*- coding: utf-8 -*-

import json
import logging
import os
import pathlib
from typing import Dict

logger = logging.getLogger("webScrapper")


class DataManager:
    def __init__(self, news_provider: str):
        self.content = {}
        self.content_unique = {}
        self.output_path = (
            pathlib.Path().absolute() / "outputs" / f"content_{news_provider}.json"
        )

    def update_content(self, new_content: Dict):
        logger.info("Updating content")
        self.content.update(new_content)

    def load_content(self, path: str = None) -> Dict:
        logger.info("Loading content")
        if path is None:
            path = self.output_path

        if os.path.exists(path):
            with open(path, "r") as fp:
                self.content = json.load(fp)
        else:
            self.content = dict()
        return self.content

    def write_content(self, path: str = None):
        logger.info("Writing content")
        if path is None:
            path = self.output_path

        with open(path, "w") as fp:
            json.dump(self.content_unique, fp)

    def remove_duplicates(self):
        logger.info("Removing duplicates")
        i = 0
        for key, value in self.content.items():
            if value not in self.content_unique.values():
                self.content_unique[i] = value
                i += 1
