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
