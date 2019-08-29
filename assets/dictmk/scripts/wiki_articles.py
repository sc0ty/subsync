#!/usr/bin/env python3
"""
    AutoCorpus: automatically extracts clean natural language corpora from
    publicly available datasets.

    articles.py: front-end to WikiParser. Reads wikipedia xml snapshots
                 from stdin and prints out the markup to stdout. Individual
                 articles are separated with the page feed character (C character \f).



    Copyright (C) 2011 Maciej Pacula


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import re
import codecs
import xml.parsers.expat as sax
from optparse import OptionParser
from wikt2dict.wiki import *
import html
from html.parser import HTMLParser

def fprint(x):
  print(x)

def save_article(htmlparser, article, directory):
  f = None
  try:
    filename = re.sub("(\s+)|/", "_", article.title.lower()) + ".txt"
    f = codecs.open(os.path.join(directory, filename), encoding='utf-8', mode='w')
    f.write(html.unescape(article.markup))
    f.write("\n")
    f.close()
  except Exception as e:
    sys.stderr.write("\nError extracting article: " + str(e) + "\n")
    if f != None:
      f.close()

def print_article(htmlparser, article):
  try:
    print("%%#PAGE " + article.title)
    print(html.unescape(article.markup))
    print("\n\n\f")
  except IOError:
    sys.exit(0) # broken stdout => broken pipe
  except Exception as e:
    sys.stderr.write("\nError extracting article: " + str(e) + "\n")

if __name__ == "__main__":
  try:
    parser = OptionParser(usage="usage: %s [-d output-directory] <stdin>" % sys.argv[0])
    parser.add_option("-d",
                      action="store", type="string", dest="directory",
                      help="directory where to store the articles")
    (options, args) = parser.parse_args()

    if len(args) > 0:
      print(parser.usage)
      exit(1)

    htmlparser = HTMLParser()
    if options.directory != None:
      do_article = lambda a: save_article(htmlparser, a, options.directory)
    else:
      do_article = lambda a: print_article(htmlparser, a)

    parser = WikiParser(do_article)
    parser.process()
    parser.close()
  except KeyboardInterrupt:
    sys.stderr.write("\n\nCancelled. Partial results may have been generated.\n")
    exit(1)
