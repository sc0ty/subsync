import data.languages


def getLanguageName(lang):
    name = data.languages.languages.get(lang, None)
    if name:
        return name[0]
    return lang


def parseVersion(version, defaultVer=None):
    try:
        return tuple(int(x) for x in version.split('.'))
    except:
        return defaultVer


def getCurrentVersion(defaultVer=None):
    try:
        from version import version_short
        return parseVersion(version_short)
    except:
        return defaultVer


def fileSizeFmt(val):
    for unit in ['B','kB','MB','GB']:
        if val < 1000.0:
            break
        val /= 1000.0
        unit = 'TB'
    return '{:.1f} {}'.format(val, unit)


def onesPositions(val):
    res = []
    idx = 0
    while val > 0:
        if val & 1:
            res.append(idx)
        idx += 1
        val >>= 1
    return res

