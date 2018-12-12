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


def timeStampFmt(time):
    t = int(time)
    h = int(t / 3600)
    m = int((t % 3600) / 60)
    s = int(t % 60)

    if t < 3600:
        return '{:d}:{:02d}'.format(m, s);
    else:
        return '{:d}:{:02d}:{:02d}'.format(h, m, s);


def timeStampFractionFmt(time):
    ms = int((time % 1) * 1000)
    return '{}.{:03d}'.format(timeStampFmt(time), ms)
