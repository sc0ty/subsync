"""
    AutoCorpus: automatically extracts clean natural language corpora from
    publicly available datasets.

    wiki.py: implements WikiParser - a fast XML parser that extracts
             markup and titles of articles from wikipedia xml snapshots.



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
import xml.parsers.expat as sax

def err(msg):
  """ Prints a message to stderr, terminating it with a newline """
  sys.stderr.write(msg + "\n")

class Article:
  """ Stores the contents of a Wikipedia article """
  def __init__(self, title, markup, is_redirect):
    self.title = title
    self.markup = markup
    self.is_redirect = is_redirect


class WikiParser:
  """Parses the Wikipedia XML and extracts the relevant data,
     such as sentences and vocabulary"""

  
  def __init__(self, callback, ignore_redirects=True):
    self.callback = callback
    self.ignore_redirects = ignore_redirects
    self.buffer_size = 10*1024*1024 # 10MB

    # Articles whose titles start with "<type>:" will be ignored.
    self.ignoredArticleTypes = ["wikipedia", "category", "template"]

    
    # setup the SAX XML parser and its callbacks
    self.xml_parser = sax.ParserCreate()
    self.xml_parser.StartElementHandler  = lambda name, attrs: self.xml_start_element(name, attrs)
    self.xml_parser.EndElementHandler    = lambda name:        self.xml_end_element(name)
    self.xml_parser.CharacterDataHandler = lambda data:        self.xml_char_data(data)

    # parser state
    self.article = None         # name of the current article
    self.section = None         # name of the current section
    self.word    = None         # current word
    self.enclosing_tags = []    # all enclosing tags (most recent first)
    self.text    = []           # contents of the current text element, in the order
                                # they come from the SAX parser
                                # (note: this is faster than concatenating on the fly)
    self.article = None         # article currently being processed

    
  def process(self):
    while True:
      buf = sys.stdin.read(self.buffer_size)
      if buf == "":
        break

      self.xml_parser.Parse(buf)
      

  def xml_char_data(self, data):
    self.text.append(data)
    pass

  def xml_start_element(self, name, attrs):
    name = name.lower()
    self.enclosing_tags = [name] + self.enclosing_tags
    self.text = []

    if name == "page":
      self.article = Article(None, None, False)

  def xml_end_element(self, name):
    name = name.lower()
    contents = "".join(self.text)

    # dispatch based on the type of the node
    if name == "title":
      self.article.title = contents
    elif name == "redirect":
      self.article.is_redirect = True
    elif name == "text":
      self.article.markup = contents
    elif name == "page":
      if self.ignore_redirects and self.article.is_redirect:
        pass
      else:
        self.new_article(self.article)
        self.article = None

    # clean up state associated with the node    
    if len(self.enclosing_tags) > 0 and name == self.enclosing_tags[0]:
      self.enclosing_tags = self.enclosing_tags[1:]
    else:
      err("Mismatched closing tag: " + name)
    self.text = []

  def new_article(self, article):
    if ':' in  article.title:
      articleType = article.title.split(':')[0].lower()
      if articleType in self.ignoredArticleTypes:
        return

    self.callback(article)

  def get_enclosing_tag(self):
    return None if len(self.enclosing_tags) == 0 else self.enclosing_tags[0]
    
  def close(self):
    """Releases all resources associated with this class"""
    pass
