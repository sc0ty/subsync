#!/usr/bin/env python3

import sys


def addToDict(d, key, val):
    if isinstance(val, set) or isinstance(val, list):
        for v in val:
            addToDict(d, key, v)
    else:
        if key not in d:
            d[key] = set()
        d[key].add(val)
    return d


def mergeDicts(d1, d2):
    res = {}
    for key in d1:
        addToDict(res, key, d1[key])
    for key in d2:
        addToDict(res, key, d2[key])
    return res


def loadDict(fname):
    d = {}
    with open(fname, 'r') as file:
        for line in file:
            if (len(line) > 0) and (line[0] != '#'):
                entrys = line.strip().split('|')
                if len(entrys) >= 2:
                    key = entrys[0]
                    if key in d:
                        print('duplicated key: "' + key + '"')
                    addToDict(d, key, entrys[1:])
                else:
                    print('invalid entry: "' + line + '"')
    return d


def saveDict(d, fname, banner=None, langs=None, version=None):
    with open(fname, 'w') as file:
        if langs and version:
            file.write('#dictionary/{}/{}/{}\n\n'.format(*langs, version))

        if banner:
            file.write(banner)
            file.write('\n\n')

        for key, vals in sorted(d.items()):
            if len(vals) > 0:
                file.write(key + '|' + '|'.join(vals) + '\n')
            else:
                print('empty translation: "' + key + '" => ()')


def transponseDict(d):
    res = {}
    for key in d:
        for val in d[key]:
            addToDict(res, val, key)
    return res


def validateDict(d):
    valsNo = 0
    err = 0
    for key in d:
        if len(key.split()) != 1:
            print('invalid key: "' + key + '"')
            err += 1
        if len(d[key]) == 0:
            print('no values for key: "' + key + '"')
            err += 1
        for val in d[key]:
            valsNo += 1
            if len(key.split()) != 1:
                print('invalid value for key "' + key + '": "' + val + '"')
                err += 1
    if err == 0:
        errs = 'No'
    else:
        errs = str(err)
    print(errs + ' errors detected, keys: ' + str(len(d)) + ', values: ' + str(valsNo))
    return err


if __name__ == "__main__":
    print('Command line tools to use with python interpreter:')
    print('\texecfile("' + sys.argv[0] + '")\n');
    print('Functions:')
    print('\tdict = loadDict(fileName)')
    print('\tsaveDict(dict, fileName)')
    print('\taddToDict(dict, key, value)')
    print('\tres = mergeDicts(dict1, dict2)')
    print('\tdict2 = transposeDict(dict)')
    print('\tvalidateDict(dict)')
