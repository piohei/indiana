import pprint


class BenchmarkLogger(object):
    @staticmethod
    def big_separator():
        print("=" * 65)

    @staticmethod
    def small_separator():
        print("-" * 65)

    def print_engine_config(self, cfg):
        self.big_separator()
        pprint.pprint(cfg)
        self.small_separator()

    def print_stamp_location(self, stamp):
        print(stamp.location)
        self.small_separator()

    @staticmethod
    def print_report(report):
        copy = report.copy()
        copy.pop("partial_reports")
        pprint.pprint(copy)