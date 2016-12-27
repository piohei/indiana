from benchmark.strategy_benchmark import StrategyBenchmark


def run(verbose=False):
    StrategyBenchmark(verbose).run()


if __name__ == '__main__':
    run(True)
