class DBException(Exception):
    def __init__(self, message):
        self.message = message


class SampleException(Exception):
    def __init__(self, message):
        self.message = message


class EngineException(Exception):
    def __init__(self, message):
        self.message = message
