import argparse
from multiprocessing import Process

from ap_data_listener.runner import run as run_ap_data_listener
from config import config
from runner.static_data.loader import StaticDataLoader

parser = argparse.ArgumentParser(description="Wifi indoor positioning system runner")


def add_flag(flag, help):
    parser.add_argument("--" + flag, dest=flag.replace("-", "_"), action="store_const",
                        help=help, const=True, default=False)

add_flag("load-static", "load static data from files")
add_flag("run-apdata-listeners", "run APData listener")


args = parser.parse_args()

if args.load_static:
    print("loading static data")
    StaticDataLoader().load()

ap_data_listeners = []
if args.run_apdata_listeners:
    for ap_data_listener_config_idx in range(len(config["ap_data"])):
        proc = Process(target=run_ap_data_listener, args=(ap_data_listener_config_idx,))
        ap_data_listeners.append(proc)
        proc.start()



