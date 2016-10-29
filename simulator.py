from collections import defaultdict

from positioning.engine import Engine

from db.ap_data_dao import APDataDAO
from db.sample_stamp_dao import SampleStampDAO

from models import Time, Mac, Signal

now = 1472826262000
last_n_milis = 1000
start = 1472829045383 # 9, 8, -2
end = 1472829170586 # 5, 10, -2

# data = RSSIMeasureDAO().grouped_rssi_stats(start, end)
# calculated_measures = {}
# for band in data.keys():
#     calculated_measures[band] = defaultdict(lambda: { "rssi1": None })
#     for mac in data[band].keys():
#         calculated_measures[band][mac]["rssi1"] = data[band][mac]["rssi1"]["avg"]

# ap_data_dao = APDataDAO()

# res = ap_data_dao.group_by_mac_and_signal_for_range(Time(start), Time(end))
# res = ap_data_dao.stats_group_by_mac_and_signal_for_range(Time(start), Time(end))

location_5_2_minus_2 = {
    Mac("F8:E7:1E:29:05:00"): {
        Signal(band="2.4", channel=2): {
            "1": -64,
        }
    },
    Mac("94:F6:65:04:E6:10"): {
        Signal(band="2.4", channel=2): {
            "1": -110,
        }
    },
    Mac("2C:5D:93:0C:8A:60"): {
        Signal(band="2.4", channel=2): {
            "1": -95,
        }
    },
    Mac("94:F6:65:05:C0:D0"): {
        Signal(band="2.4", channel=2): {
            "1": -75,
        }
    },
    Mac("94:F6:65:04:FF:D0"): {
        Signal(band="2.4", channel=2): {
            "1": -66,
        }
    },
    Mac("94:F6:65:04:F9:40"): {
        Signal(band="2.4", channel=2): {
            "1": -71,
        }
    },
    Mac("94:F6:65:08:7B:60"): {
        Signal(band="2.4", channel=2): {}
    },
    Mac("F8:E7:1E:29:0E:E0"): {
        Signal(band="2.4", channel=2): {
            "1": -82,
        }
    },
    Mac("F8:E7:1E:29:08:F0"): {
        Signal(band="2.4", channel=2): {
            "1": -110,
        }
    }
}

# measures = calculated_measures
measures = location_5_2_minus_2

en = Engine(chain='beta', params={
    'ap_data_dao': APDataDAO(),
    'sample_stamp_dao': SampleStampDAO(),
    'measures': measures
})

res = en.calculate()
# print(measures)
print(res)
# res = en.calculate()[0]
# for sample in res:
#     print(sample.stamp.location, sample.ap_data_by_band_and_mac)
