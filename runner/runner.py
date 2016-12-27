import argparse
from multiprocessing import Process

from config import config

parser = argparse.ArgumentParser(description="Wifi indoor positioning system runner")


def add_flag(flag, help):
    parser.add_argument("--" + flag, dest=flag.replace("-", "_"), action="store_const",
                        help=help, const=True, default=False)

add_flag("load-static", "Load static data from files")
add_flag("run-apdata-listeners", "Run APData listeners")
add_flag("run-web", "Run web management and visualisation")
add_flag("run-positioning", "Run positioning engine(s)")


args = parser.parse_args()

if args.load_static:
    from runner.static_data.loader import StaticDataLoader
    print("loading static data")
    StaticDataLoader().load()

ap_data_listeners = []
if args.run_apdata_listeners:
    from ap_data_listener.runner import run as run_ap_data_listener
    for ap_data_listener_config_idx in range(len(config["ap_data"])):
        proc = Process(target=run_ap_data_listener, args=(ap_data_listener_config_idx,))
        ap_data_listeners.append(proc)
        proc.start()

web = None
if args.run_web:
    from web.runner import run as run_web
    web = Process(target=run_web)
    web.start()

engines = []
if args.run_positioning:
    from positioning.runner import run as run_engine
    for engine_id in range(len(config["engine"]["instances"])):
        proc = Process(target=run_engine, args=(config["engine"], engine_id))
        engines.append(proc)
        proc.start()

