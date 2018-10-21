import data.languages


def getLanguageName(lang):
    name = data.languages.languages.get(lang, None)
    if name:
        return name[0]
    return lang


def parvseVersion(version):
    try:
        return tuple(int(x) for x in version.split('.'))
    except:
        return None


def getCurrentVersion():
    try:
        from version import version_short
        return parvseVersion(version_short)
    except:
        return None


def fileSizeFmt(val):
    for unit in ['B','kB','MB','GB']:
        if val < 1000.0:
            break
        val /= 1000.0
        unit = 'TB'
    return '{:.1f} {}'.format(val, unit)
