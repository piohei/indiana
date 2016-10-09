# -*- coding: utf-8 -*-


class Signal(object):
    def __init__(self, channel, band='2.4'):
        if type(channel) != int:
            raise ValueError('Argument channel must be int')

        if type(band) != str or band not in ['2.4', '5']:
            raise ValueError('Argument band must be one of: "2.4", "5"')

        valid_24 = list(range(1, 13+1))
        valid_5  = list(range(34, 64+1, 2)) + \
                   list(range(100, 144+1, 2)) + \
                   list(range(149, 161+1, 2)) + \
                   list([165])

        if band == '2.4' and channel not in valid_24:
            raise ValueError('Argument channel must be in range {}'.format(valid_24))
        elif band == '5' and channel not in valid_5:
            raise ValueError('Argument channel must be in range {}'.format(valid_24))

        self.channel = channel
        self.band = band

    def __str__(self, *args, **kwargs):
        return '(channel={}, band={} GHz)'.format(self.channel, self.band)

    def __repr__(self):
        return '"{}"'.format(str(self))

    def __eq__(self, other):
        return self.channel == other.channel and self.band == self.band

    def __hash__(self):
        return hash("{}{}".format(self.channel, self.band))
