import numpy as np


class ToClustersOfNClosestSamples(object):
    def __init__(self, cluster_n_closest, **kwargs):
        self.n = int(cluster_n_closest)

    def clusterise(self, sample, all_samples):
        loc = sample.location()
        dists = np.array([loc.distance_from(s.location()) for s in all_samples])
        cluster_indices = dists.argsort()[:self.n + 1]
        return [all_samples[i] for i in cluster_indices]

    def calculate(self, samples, **kwargs):
        clusters = {str(sample.stamp.location): self.clusterise(sample, samples) for sample in samples}
        return {"samples_clusters": clusters}
