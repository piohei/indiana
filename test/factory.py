from models import *


def create_ap_data(
        router_mac=Mac('11:12:13:14:15:16'),
        device_mac=Mac('A1:A2:A3:A4:A5:A6'),
        created_at=Time(1),
        rssis={ '1': RSSI(-20) },
        signal=Signal(channel=2, band='2.4')
    ):
    return APData(
        router_mac=router_mac,
        device_mac=device_mac,
        created_at=created_at,
        rssis=rssis,
        signal=signal
    )

def create_sample_stamp(
        mac=Mac('A1:A2:A3:A4:A5:A6'),
        location=Location(0, 0, 0),
        start_time=Time(1),
        end_time=Time(2)
    ):
    return SampleStamp(
        mac=mac,
        location=location,
        start_time=start_time,
        end_time=end_time
    )

def ap_data_post_data(rss1=1, time=1, band=1, apMac='111213141516'):
    return {
        'data': [{
            'rss1': rss1,
            'rss2': rss1+1,
            'rss3': rss1+2,
            'clientMac': 'DCEE0661B03D'
        }],
        'time': time,
        'band': band,
        'apMac': str(apid)
    }
