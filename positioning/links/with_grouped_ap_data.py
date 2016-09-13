from models.ap_data import APData

class WithGroupedApData(object):

    @staticmethod
    def group_for(fingertip):
        return {"fingertip": fingertip, "ap_data": APData.group_for_fingertip(fingertip)}

    def calculate(self, fingertips):
        return map(self.group_for, fingertips)
