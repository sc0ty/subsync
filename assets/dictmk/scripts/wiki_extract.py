#!/usr/bin/env python3
from wikt2dict.wiktionary import Wiktionary
import wikt2dict.config
import sys

cfgs = [ cfg for cfg in wikt2dict.config.configs if cfg.wc == sys.argv[1] ]

if cfgs:
    cfg = cfgs[0]

    cfg.dump_path = sys.argv[2]
    cfg.output_path = sys.argv[3]

    wikt = Wiktionary(cfg)
    wikt.parse_articles()
