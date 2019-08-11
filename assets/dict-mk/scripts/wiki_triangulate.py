#!/usr/bin/env python3
from wikt2dict.triangulator import Triangulator
import wikt2dict.config
import sys, os

src_dir = sys.argv[1]
dst_dir = sys.argv[2]
langs = sys.argv[3:6]

for lang in langs:
    cfgs = [ cfg for cfg in wikt2dict.config.configs if cfg.wc == lang ]
    if cfgs:
        cfg = cfgs[0]
        cfg.output_path = os.path.join(src_dir, lang + '.2')

triangulator = Triangulator(langs)
triangulator.collect_triangles()
triangulator.write_triangles(dst_dir)
