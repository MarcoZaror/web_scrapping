# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:34:59 2020

@author: Marco
"""

import json
import os

class Data:
    def __init__(self):
        self.content = {}
        self.cont_uniq = {}
    
    def update_content(self, new_content):
        self.content.update(new_content)
        #return self.content
    
    def load_content(self, path):
        if os.path.exists(path):
            with open(path, 'r') as fp:
                self.content = json.load(fp)
        return self.content
    
    def write_content(self, path):
        with open(path, 'w') as fp:
            json.dump(self.cont_uniq, fp)
    
    def remove_dup(self):
        i=0
        for key,value in self.content.items():
            if value not in self.cont_uniq.values():
                self.cont_uniq[i] = value
                i += 1
        #return self.cont_uniq
        
            
'''            
result_dm = {}
i=0
for key,value in data_dm.items():
    if value not in result_dm.values():
        result_dm[i] = value
        i += 1
'''