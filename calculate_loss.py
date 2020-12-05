#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:23:01 2020

@author: luokai
"""

import torch
from torch import nn
import numpy as np


class Calculate_loss():
    def __init__(self, label_dict):
        self.loss = nn.CrossEntropyLoss()
        self.label2idx = dict()
        self.idx2label = dict()
        for key in ['TNEWS', 'OCNLI', 'OCEMOTION']:
            self.label2idx[key] = dict()
            self.idx2label[key] = dict()
            for i, e in enumerate(label_dict[key]):
                self.label2idx[key][e] = i
                self.idx2label[key][i] = e
    
    def idxToLabel(self, key, idx):
        return self.idx2Label[key][idx]
    
    def labelToIdx(self, key, label):
        return self.label2idx[key][label]
    
    def compute(self, tnews_pred, ocnli_pred, ocemotion_pred, tnews_gold, ocnli_gold, ocemotion_gold):
        res = 0
        if tnews_pred != None:
            res += self.loss(tnews_pred, tnews_gold)
        if ocnli_pred != None:
            res += self.loss(ocnli_pred, ocnli_gold)
        if ocemotion_pred != None:
            res += self.loss(ocemotion_pred, ocemotion_gold)
        return res
    
    def correct_cnt(self, tnews_pred, ocnli_pred, ocemotion_pred, tnews_gold, ocnli_gold, ocemotion_gold):
        good_nb = 0
        total_nb = 0
        if tnews_pred != None:
            tnews_val = torch.argmax(tnews_pred, axis=1)
            for i, e in enumerate(tnews_gold):
                if e == tnews_val[i]:
                    good_nb += 1
                total_nb += 1
        if ocnli_pred != None:
            ocnli_val = torch.argmax(ocnli_pred, axis=1)
            for i, e in enumerate(ocnli_gold):
                if e == ocnli_val[i]:
                    good_nb += 1
                total_nb += 1
        if ocemotion_pred != None:
            ocemotion_val = torch.argmax(ocemotion_pred, axis=1)
            for i, e in enumerate(ocemotion_gold):
                if e == ocemotion_val[i]:
                    good_nb += 1
                total_nb += 1
        return good_nb, total_nb
    
    def collect_pred_and_gold(self, pred, gold):
        if pred == None or gold == None:
            p, g = [], []
        else:
            p, g = np.array(torch.argmax(pred, axis=1).cpu()).tolist(), np.array(gold.cpu()).tolist()
        return p, g