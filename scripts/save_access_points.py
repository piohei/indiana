from db.access_point_dao import AccessPointDAO
from models.access_point import AccessPoint
from models.primitives.location import Location
from models.primitives.mac import Mac

ap_dao = AccessPointDAO()

access_points = [
    AccessPoint(1, "blue toddler", Location(32.5, 0.5, 0), Mac("94:f6:65:04:e6:10"), True),
    AccessPoint(2, "miss molly", Location(32.5, 11.75, 0), Mac("94:f6:65:08:7b:60"), True),
    AccessPoint(3, "big wilson", Location(26.65, 11.75, 0), Mac("f8:e7:1e:29:08:f0"), True),
    AccessPoint(4, "dirty genius", Location(20.75, 6.75, 0), Mac("2c:5d:93:0c:8a:60"), True),
    AccessPoint(5, "fast mandy", Location(12.25, 11.75, 0), Mac("f8:e7:1e:29:0e:e0"), True),
    AccessPoint(6, "koko brutal", Location(10.9, 6.75, 0), Mac("94:f6:65:04:f9:40"), True),
    AccessPoint(7, "mister sun", Location(4, 11.75, 0), Mac("94:f6:65:05:c0:d0"), True),
    AccessPoint(8, "miss dino", Location(9.1, 0.5, 0), Mac("f8:e7:1e:29:05:00"), False),
    AccessPoint(9, "black megan", Location(0.5, 0.5, 0), Mac("94:f6:65:04:ff:d0"), True),
]

for ap in access_points:
    ap_dao.save(ap)
