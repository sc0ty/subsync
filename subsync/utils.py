def parseVersion(version, defaultVer=None):
    try:
        return tuple(int(x) for x in version.split('.'))
    except:
        return defaultVer


def versionToString(version, defaultVer=None):
    try:
        return '.'.join([ str(v) for v in version ])
    except:
        return defaultVer


def getCurrentVersion(defaultVer=None):
    try:
        from subsync.version import version_short
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


def transferSpeedFmt(size, interval):
    return '{}/s'.format(fileSizeFmt(size / interval))


def timeStampFmt(time):
    try:
        t = int(time)
        h = int(t / 3600)
        m = int((t % 3600) / 60)
        s = int(t % 60)

        if t < 3600:
            return '{:d}:{:02d}'.format(m, s)
        else:
            return '{:d}:{:02d}:{:02d}'.format(h, m, s)
    except:
        return '-'


def timeStampFractionFmt(time):
    try:
        ms = int((time % 1) * 1000)
        return '{}.{:03d}'.format(timeStampFmt(time), ms)
    except:
        return '-'


def timeStampApproxFmt(time):
    try:
        h = time / 3600
        if h >= 0.9:
            return _('{} hours').format(round(max(h, 1)))
        m = time / 60
        if m <= 1:
            return _('less than minute')
        if m >= 15:
            m = round(m / 5) * 5
        else:
            m = round(m)
        if m == 1:
            return _('1 minute')
        else:
            return _('{} minutes').format(m)
    except:
        return '-'


def fmtobj(name, *args, **kw):
    return '{}({})'.format(name, fmtstr(*args, **kw))


def fmtstr(*args, **kw):
    items  = [ str(arg) for arg in args if arg ]
    items += [ '{}={}'.format(k, v) for k, v in kw.items() if v ]
    return ', '.join(items)
