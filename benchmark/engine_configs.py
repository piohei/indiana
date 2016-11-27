full_linear_regression_config = {
    "strategy_name": "FullLinearRegression"
}

one_nn_permutations_config = {
    "strategy_name": "1-NN",
    "strategy_config": {
        "chain": "permutations",
        "ap_data_per_ap": 2
    }
}

one_nn_beta_config = {
    "strategy_name": "1-NN",
    "strategy_config": {
        "chain": "beta"
    }
}

one_nn_consecutive_config = {
    "strategy_name": "1-NN",
    "strategy_config": {
        "chain": "consecutive"
    }
}

one_nn_beta_linreg_config = {
    "strategy_name": "1-NNWithLinearRegression",
    "strategy_config": {
        "chain": "beta",
        "cluster_n_closest": 8
    }
}

one_nn_consecutive_linreg_config = {
    "strategy_name": "1-NNWithLinearRegression",
    "strategy_config": {
        "chain": "consecutive",
        "cluster_n_closest": 8
    }
}

one_nn_permutations_linreg_config = {
    "strategy_name": "1-NNWithLinearRegression",
    "strategy_config": {
        "chain": "permutations",
        "ap_data_per_ap": 2,
        "cluster_n_closest": 8
    }
}

configs = [full_linear_regression_config,
           one_nn_beta_config,
           one_nn_consecutive_config,
           one_nn_permutations_config,
           one_nn_beta_linreg_config,
           one_nn_consecutive_linreg_config,
           one_nn_permutations_linreg_config]
