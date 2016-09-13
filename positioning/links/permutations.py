from collections import defaultdict

class Permutations(object):
    @staticmethod
    def rssis_only(dictionary):
        return {key: dictionary[key] for key in ["rss1", "rss2", "rss3"]}

    @staticmethod
    def functional_add(key, value, dictionary):
        new = dict(dictionary)
        new[key] = value
        return value

    def permutate(self, source_dict, keys_left):
        if not keys_left:
            return [{}]
        else:
            ap_mac, *tail = keys_left
            partial_results = self.permutate(source_dict, tail)
            rssis = source_dict[ap_mac]
            return [self.functional_add(ap_mac, rssi, partial) for rssi in rssis for partial in partial_results]

    def to_complete_fingertips(self, macs_to_rssis, location):
        return [{"data": data, "location": location} for data in self.permutate(macs_to_rssis, macs_to_rssis.keys())]

    def calculate(self, fingertips_with_ap_data):
        result = defaultdict(list)
        for fingertip_with_ap_data in fingertips_with_ap_data:
            location = fingertip_with_ap_data["fingertip"].location

            ap_data_by_band = defaultdict(dict)
            for ap_data in fingertip_with_ap_data["ap_data"]:
                ap_data_by_band[ap_data["band"]][ap_data["apMac"]] = map(self.rssis_only, ap_data["data"])

            for band, macs_to_rssis in  ap_data_by_band.items():
                result[band].extend(self.to_complete_fingertips(macs_to_rssis, location))

        return result


