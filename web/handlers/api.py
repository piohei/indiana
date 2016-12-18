from web.handlers import api_handlers

class API(object):
    def __init__(self, config, daos):
        self.access_point_dao = daos["access_point_dao"]
        self.sample_stamp_dao = daos["sample_stamp_dao"]
        self.benchmark_report_dao = daos["benchmark_report_dao"]
        self.map_dao = daos["map_dao"]

        self.map_data = self.map_dao.find_by_name(config['map']['name'])

    def get_handlers(self, config):
        prefix = config["web"]["routes"]["api"]["prefix"]
        endpoints = config["web"]["routes"]["api"]["endpoints"]
        return [
            (prefix + endpoints["report_map"] + "/([^/]+)", api_handlers.ReportMapHandler, {
                'access_point_dao': self.access_point_dao,
                'benchmark_report_dao': self.benchmark_report_dao,
                'map_data': self.map_data
            }),
            (prefix + endpoints["map"], api_handlers.MapHandler, {
                'access_point_dao': self.access_point_dao,
                'sample_stamp_dao': self.sample_stamp_dao,
                'map_data': self.map_data
            })
        ]