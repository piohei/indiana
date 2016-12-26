from web.modules.api import handlers
from web.modules.handlers_module import HandlersModule


class API(HandlersModule):
    def module(self):
        return "api"

    def __init__(self, config, daos):
        super().__init__(config)
        self.access_point_dao = daos["access_point_dao"]
        self.sample_stamp_dao = daos["sample_stamp_dao"]
        self.benchmark_report_dao = daos["benchmark_report_dao"]
        self.map_dao = daos["map_dao"]

        self.map_data = self.map_dao.find_by_name(config['map']['name'])

    def get_handlers(self, config):
        return [
            (self.prefix + self.endpoints["report_map"] + "/([^/]+)", handlers.ReportMapHandler, {
                'access_point_dao': self.access_point_dao,
                'benchmark_report_dao': self.benchmark_report_dao,
                'map_data': self.map_data
            }),
            (self.prefix + self.endpoints["map"], handlers.MapHandler, {
                'access_point_dao': self.access_point_dao,
                'sample_stamp_dao': self.sample_stamp_dao,
                'map_data': self.map_data
            })
        ]