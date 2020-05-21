subtitleTypes = [
        { 'type': 'srt', 'ext': '.srt', 'name': 'SubRIP' },
        { 'type': 'ssa', 'ext': '.ssa', 'name': 'Sub Station Alpha' },
        { 'type': 'ass', 'ext': '.ass', 'name': 'Advanced SSA' },
        { 'type': 'microdvd', 'ext': '.sub', 'name': 'MicroDVD' },
        { 'type': 'tmp', 'ext': '.txt', 'name': 'TMP' },
]

videoExt = [
        '.webm', '.mkv', '.flv', '.vob', '.ogv', '.avi', '.mov',
        '.qt', '.wmv', '.rm', '.rmvb', '.asf', '.amv', '.mp4',
        '.m4p', '.m4v', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv',
        '.mpg', '.mpeg', '.m2v', '.m4v', '.3gp', '.3g2', '.f4v',
        '.f4p', '.f4a', '.f4b',
]

subtitleWildcard = ';'.join('*' + x['ext'] for x in subtitleTypes)
videoWildcard = ';'.join('*{}'.format(x) for x in videoExt)

