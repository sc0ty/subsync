#!/usr/bin/env python3
import sys
import os
import re
import glob
import json
import zipfile

src_dir = sys.argv[1]
dst_path = sys.argv[2]
base_url = sys.argv[3]

index = {}

dict_re    = re.compile(r'^dict-(...)-(...).zip$')
speech_re  = re.compile(r'^speech-(...).zip$')
upgrade_re = re.compile(r'^subsync-([0-9]+\.[0-9]+\.[0-9]+)-(.+).zip$')

for src_path in glob.glob(os.path.join(src_dir, 'dict-*.zip')):
    fname = os.path.basename(src_path)
    n = dict_re.search(fname)
    lang1, lang2 = n.group(1), n.group(2)

    zipf = zipfile.ZipFile(src_path, 'r', zipfile.ZIP_DEFLATED)
    banner = zipf.read('dict/{}-{}.dict'.format(lang1, lang2)).split(maxsplit=1)[0].decode('utf8')
    ents = banner.strip().split('/')
    assert(ents[0] == '#dictionary')
    assert(ents[1] == lang1)
    assert(ents[2] == lang2)
    version = ents[3]

    index['dict/{}-{}'.format(lang1, lang2)] = {
            'type': 'zip',
            'url': base_url + fname,
            'sig': base_url + fname + '.asc',
            'version': version,
            }

for src_path in glob.glob(os.path.join(src_dir, 'speech-*.zip')):
    fname = os.path.basename(src_path)
    n = speech_re.search(fname)
    lang = n.group(1)

    zipf = zipfile.ZipFile(src_path, 'r', zipfile.ZIP_DEFLATED)
    data = zipf.read('speech/{}.speech'.format(lang)).decode('utf8')
    speech = json.loads(data)
    assert(speech['lang'] == lang)
    version = speech['version']

    index['speech/{}'.format(lang)] = {
            'type': 'zip',
            'url': base_url + fname,
            'sig': base_url + fname + '.asc',
            'version': version,
            }

for src_path in glob.glob(os.path.join(src_dir, 'subsync-*.zip')):
    fname = os.path.basename(src_path)
    n = upgrade_re.search(fname)
    lang = n.group(1)
    arch = n.group(2)

    zipf = zipfile.ZipFile(src_path, 'r', zipfile.ZIP_DEFLATED)
    data = zipf.read('upgrade/upgrade.json').decode('utf8')
    upgrade = json.loads(data)
    version = upgrade['version']

    index['subsync/{}'.format(arch)] = {
            'type': 'zip',
            'url': base_url + fname,
            'sig': base_url + fname + '.asc',
            'version': version,
            }

with open(dst_path, 'w', encoding='utf8') as fp:
    json.dump(index, fp, indent=4, sort_keys=True)
