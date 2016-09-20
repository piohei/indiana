from models import SampleStamp


def loc(x):
    return {"x": x, "y": x, "z": x}


def stamp(location, st=1, **kwargs):
    et = kwargs["et"] if "et" in kwargs else st+2
    return SampleStamp(mac="1", location=location, start_time=st, end_time=et)