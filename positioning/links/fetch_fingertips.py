from models.fingertip import Fingertip


class FetchFingertips(object):
    def calculate(self):
        return Fingertip.find_all()
