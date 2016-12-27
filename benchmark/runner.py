import psutil
import signal

from benchmark.strategy_benchmark import StrategyBenchmark


def run(verbose=False):
    StrategyBenchmark(verbose).run()


def kill(process):
    pid = process.pid
    print("PIDPIDPIDPID", pid)
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return False
    children = parent.children(recursive=True)
    for child in children:
        child.send_signal(signal.SIGTERM)
    process.terminate()
    return True



if __name__ == '__main__':
    run(True)
