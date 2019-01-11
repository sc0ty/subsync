#!/usr/bin/env python3

import os


class Dictionary(object):
    def __init__(self, path=None, lang1=None, lang2=None, version=None, banner=None):
        self.d = {}
        self.lang1 = lang1
        self.lang2 = lang2
        self.version = version
        self.banner = banner

        if path:
            self.load(path)

    def add(self, key, val):
        if isinstance(val, set) or isinstance(val, list):
            for v in val:
                self.add(key, v)
        else:
            if key not in self.d:
                self.d[key] = set()
            self.d[key].add(val)

    def merge(self, other):
        for key, val in other.d.items():
            self.add(key, val)

    def load(self, path):
        self.d = {}
        with open(path, 'r', encoding='utf8') as fp:
            parse_header(fp, self)
            self.banner = parse_banner(fp)

            for line in fp:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    entrys = line.strip().split('|')
                    if len(entrys) >= 2:
                        key = entrys[0]
                        if key in self.d:
                            print('duplicated key: "' + key + '"')
                        self.add(key, entrys[1:])
                    else:
                        print('invalid entry: "' + line + '"')

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf8') as fp:
            if self.lang1 and self.lang2 and self.version:
                fp.write('#dictionary/{}/{}/{}\n\n'.format(self.lang1, self.lang2, self.version))

            if self.banner:
                fp.write(self.banner)
                fp.write('\n\n')

            for key, vals in sorted(self.d.items()):
                if len(vals) > 0:
                    fp.write(key + '|' + '|'.join(sorted(vals)) + '\n')
                else:
                    print('empty translation: "' + key + '" => ()')

    def get_name(self):
        if self.lang1 and self.lang2:
            return '{}-{}.dict'.format(self.lang1, self.lang2)

    def transpose(self):
        res = Dictionary(lang2=self.lang1, lang1=self.lang2, version=self.version, banner=self.banner)
        for key in self.d:
            for val in self.d[key]:
                res.add(val, key)
        return res

    def validate(self):
        valsNo = 0
        err = 0
        for key in self.d:
            if not key or len(key.split()) != 1:
                print('invalid key: "' + key + '"')
                err += 1
            if len(self.d[key]) == 0:
                print('no values for key: "' + key + '"')
                err += 1
            for val in self.d[key]:
                valsNo += 1
                if len(key.split()) != 1:
                    print('invalid value for key "' + key + '": "' + val + '"')
                    err += 1
        if err == 0:
            errs = 'No'
        else:
            errs = str(err)
        print(errs + ' errors detected, keys: ' + str(len(self.d)) + ', values: ' + str(valsNo))
        return err

    def __repr__(self):
        return 'Dictionary {}/{} {} {} keys'.format(self.lang1, self.lang2, self.version, len(self.d))

    def __len__(self):
        return len(self.d) if self.d else 0


def parse_header(fp, d):
    h = fp.readline().strip()
    if h[0] == '#':
        ents = h.split('/', 3)
        if len(ents) == 4 and ents[0] == '#dictionary':
            d.lang1 = ents[1]
            d.lang2 = ents[2]
            d.version = ents[3]
            return True

    fp.seek(0)
    return False


def parse_banner(fp):
    banner = []
    for line in fp:
        line = line.strip()
        if len(line) > 0 and line[0] != '#':
            break
        banner.append(line)
    fp.seek(0)

    if banner:
        return '\n'.join(banner)
    else:
        return None

