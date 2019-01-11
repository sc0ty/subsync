#!/usr/bin/env python3

import sys
import sqlite3
from dict_tools import Dictionary


def readDictFromSqliteDB(d, fname):
    db = sqlite3.connect(fname)
    cursor = db.cursor()
    cursor.execute('select written_rep, trans_list from translation')
    #where part_of_speech in (
        #'noun', 'properNoun', 'adjective', 'adverb', 'interjection',
        #'possessiveAdjective', 'conjunction', 'verb', 'particle', 'preposition',
        #'modal', 'pronoun', 'indefinitePronoun', 'numeral',
        #'interrogativePronoun', 'indefiniteCardinalNumeral',
        #'multiplicativeNumeral', 'personalPronoun', 'cardinalNumeral',
        #'collective', 'participleAdjective', 'numeralFraction'); ''')
    for row in cursor:
        key = row[0].strip()
        vals = row[1].split('|')
        if key.find(' ') == -1:
            for val in vals:
                val = val.strip()
                if ' ' not in val:
                    d.add(key, val)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        d = Dictionary()
        readDictFromSqliteDB(d, sys.argv[1])
        d.validate()
        d.save(sys.argv[2])
    else:
        print('Usage:')
        print('\t' + sys.argv[0] + ' infile.sqlite3 outfile.dict')
