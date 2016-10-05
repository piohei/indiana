from collections import defaultdict

from db.db import db
from db.ap_data_dao import APDataDAO
from models.rssi_measure import TimedRSSIMeasure


class RSSIMeasureDAO(object):
    @staticmethod
    def collection_name():
        return APDataDAO.collection_name()

    def grouped_timed_measures_for_range(self, start_time, end_time):
        grouped = db[self.collection_name()].group(
            collection=self.collection_name(),
            key=["apMac", "band"],
            condition={
                "time": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            },
            initial={"ap_data": []},
            reduce="""function(curr, result) {
                      var o = curr.data[0];
                      var mapped = {rss1: o.rss1, rss2: o.rss2, rss3: o.rss3, time: curr.time};
                      result.ap_data.push(mapped);
                  }"""
        )

        ap_data_by_band_and_mac = defaultdict(dict)
        for ap_data in grouped:
            measures = list(map(lambda a: TimedRSSIMeasure(**a), ap_data["ap_data"]))
            ap_data_by_band_and_mac[ap_data["band"]][ap_data["apMac"]] = measures

        return ap_data_by_band_and_mac

    def grouped_rssi_stats(self, start_time, end_time):
        grouped = db[self.collection_name()].group(
            collection=self.collection_name(),
            key=["apMac", "band"],
            condition={
                "time": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            },
            initial={
                "measures": {
                    "rssi1": [],
                    "rssi2": [],
                    "rssi3": []
                }
            },
            reduce="""function(curr, result) {
                      var o = curr.data[0];
                      if(o.rss1) result.measures.rssi1.push(o.rss1);
                      if(o.rss2) result.measures.rssi2.push(o.rss2);
                      if(o.rss3) result.measures.rssi3.push(o.rss3);
                  }"""
        )

        ap_data_by_band_and_mac = defaultdict(dict)
        for ap_data in grouped:
            l1 = ap_data["measures"]["rssi1"]
            l2 = ap_data["measures"]["rssi2"]
            l3 = ap_data["measures"]["rssi3"]
            ap_data_by_band_and_mac[ap_data["band"]][ap_data["apMac"]] = {
                "rssi1": {
                    "min": min(l1) if l1 else None,
                    "max": max(l1) if l1 else None,
                    "avg": sum(l1) / float(len(l1)) if l1 else None
                },
                "rssi2": {
                    "min": min(l2) if l2 else None,
                    "max": max(l2) if l2 else None,
                    "avg": sum(l2) / float(len(l2)) if l2 else None
                },
                "rssi3": {
                    "min": min(l3) if l3 else None,
                    "max": max(l3) if l3 else None,
                    "avg": sum(l3) / float(len(l3)) if l3 else None
                }
            }

        return ap_data_by_band_and_mac
