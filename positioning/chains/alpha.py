# -*- coding: utf-8 -*-

import links

class Alpha:
    def __init__(self, *args):
        pass

    def calculate(self, *args):
        res = args

        res = links.pass_args.calculate(*res)
        res = links.pass_args.calculate(*res)

        return res
