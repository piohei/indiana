import argparse

from runner.static_data.loader import StaticDataLoader

parser = argparse.ArgumentParser(description="Wifi indoor positioning system runner")
parser.add_argument("--load-static", dest="load_static", action='store_const',
                    help="load static data from files",
                    const=True, default=False)

args = parser.parse_args()
if args.load_static:
    print("loading static data")
    StaticDataLoader().load()
