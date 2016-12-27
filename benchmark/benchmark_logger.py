import pprint


class BenchmarkLogger(object):
    def __init__(self, verbose):
        self.verbose = verbose

    def big_separator(self):
        if self.verbose:
            print("=" * 65)

    def small_separator(self):
        if self.verbose:
            print("-" * 65)

    def print_engine_config(self, cfg):
        if self.verbose:
            self.big_separator()
            pprint.pprint(cfg)
            self.small_separator()

    def print_stamp_location(self, stamp):
        if self.verbose:
            print(stamp.location)
            self.small_separator()

    def print_report(self, report):
        if self.verbose:
            copy = report.copy()
            copy.pop("partial_reports")
            pprint.pprint(copy)