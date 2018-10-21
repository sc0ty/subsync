subtitleTypes = (
        ('SubRIP', '*.srt'),
        ('MicroDVD', '*.txt'),
        ('Sub Station Alpha', '*.ssa'),
        ('Advanced SSA', '*.ass'))

videoExt = (
        '*.webm', '*.mkv', '*.flv', '*.vob', '*.ogv', '*.avi', '*.mov',
        '*.qt', '*.wmv', '*.rm', '*.rmvb', '*.asf', '*.amv', '*.mp4',
        '*.m4p', '*.m4v', '*.mpg', '*.mp2', '*.mpeg', '*.mpe', '*.mpv',
        '*.mpg', '*.mpeg', '*.m2v', '*.m4v', '*.3gp', '*.3g2', '*.f4v',
        '*.f4p', '*.f4a', '*.f4b')

subtitleWildcard = ';'.join(x[1] for x in subtitleTypes)
videoWildcard = ';'.join(videoExt)

