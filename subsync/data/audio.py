# ids from ffmpeg libavutil/channel_layout.h

audioChannelNames = {
        0: _('front left'),
        1: _('front right'),
        2: _('front center'),
        3: _('subwoofer'),
        4: _('back left'),
        5: _('back right'),
        6: _('front left of center'),
        7: _('front right of center'),
        8: _('back center'),
        9: _('side left'),
        10: _('side right'),
        11: _('top center'),
        12: _('top front left'),
        13: _('top front center'),
        14: _('top front right'),
        15: _('top back left'),
        16: _('top back center'),
        17: _('top back right'),
        29: _('stereo left'),
        30: _('stereo right'),
        31: _('wide left'),
        32: _('wide right'),
        33: _('surround direct left'),
        34: _('surround direct right'),
        35: _('second subwoofer'),
}


def getAduioChannelName(id):
    return audioChannelNames.get(id, _('channel {}'.format(id)))

