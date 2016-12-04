from positioning.links.transform import ToLinRegData


class ToLinRegDataPerLocation(object):
    def __init__(self, **kwargs):
        self.to_lin_reg_data = ToLinRegData(**kwargs)

    def calculate(self, samples_clusters, **kwargs):
        lin_reg_data_per_location = {loc_str: self.to_lin_reg_data.calculate(cluster)["lin_reg_datas"]
                                     for loc_str, cluster in samples_clusters.items()}
        return {"lin_reg_data_per_location": lin_reg_data_per_location}
