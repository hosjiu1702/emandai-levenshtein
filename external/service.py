"""
This serivce re-use Python-Levenshtein package
from https://github.com/ztane/python-Levenshtein.

It uses FastAPI to build the service which computes
Levenshtein distance between two given sentences.

    Author: @hosjiu (hosjiu1702@gmail.com)

"""
from typing import List, Text
import logging

from pyvi import ViTokenizer
from fastapi import FastAPI
from pydantic import BaseModel
from Levenshtein.StringMatcher import StringMatcher


# LOGGING
logging.basicConfig(level=logging.DEBUG)


# INSTANTIATE FASTAPI APP
app = FastAPI()


class TextPairs(BaseModel):
    data: List[Text]


@app.post("/levenshtein/get_ratio")
async def compute_lev_dist(text_pairs: TextPairs):
    ret = []
    try:
        for text_pair in text_pairs.data:
            tmp_dict = {}

            # Parse + Sanitize
            seq1, seq2 = text_pair.split(";")
            seq1 = seq1.strip()
            seq2 = seq2.strip()

            # Tokenize
            seq1 = ViTokenizer.tokenize(seq1)
            seq2 = ViTokenizer.tokenize(seq2)

            # Levenshtein here
            str_matcher = StringMatcher(seq1=seq1, seq2=seq2)

            ratio = str_matcher.ratio()
            tmp_dict.update({text_pair: ratio})
            ret.append(tmp_dict)

        return ret
    except Exception:
        logging.error("[ERROR]", exc_info=True)
        return {"status": "Maybe bug or something else???"}
