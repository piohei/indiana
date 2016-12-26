from web.handlers.api import handlers
from web.handlers.api.handlers.path_handler import PathHandler
from web.handlers.api.handlers.stamp.benchmark_stamp_handler import BenchmarkStampHandler
from web.handlers.api.handlers.stamp.sample_stamp_handler import SampleStampHandler
from web.handlers.handlers_module import HandlersModule


class API(HandlersModule):
    def module(self):
        return "api"

    def __init__(self, config, daos, services):
        super().__init__(config)
        self.access_point_dao = daos["access_point_dao"]
        self.sample_stamp_dao = daos["sample_stamp_dao"]
        self.benchmark_stamp_dao = daos["benchmark_stamp_dao"]
        self.benchmark_report_dao = daos["benchmark_report_dao"]
        self.map_dao = daos["map_dao"]
        self.path_dao = daos["path_dao"]
        self.ap_data_dao = daos["ap_data_dao"]

        self.sample_service = services["sample_service"]
        self.log_socket_service = services["log_socket_service"]
        self.path_service = services["path_sefvice"]

        self.map_data = self.map_dao.find_by_name(config['map']['name'])

    def handlers_specs(self):
        return [
            ("report_map", handlers.ReportMapHandler, {
                'access_point_dao': self.access_point_dao,
                'benchmark_report_dao': self.benchmark_report_dao,
                'map_data': self.map_data
            }),
            ("map", handlers.MapHandler, {
                'access_point_dao': self.access_point_dao,
                'sample_stamp_dao': self.sample_stamp_dao,
                'map_data': self.map_data
            }),
            ("sample_stamp", SampleStampHandler, {
                "sample_service": self.sample_service
            }),
            ("benchmark_stamp", BenchmarkStampHandler, {
                "sample_service": self.sample_service
            }),
            ("path", PathHandler, {
                "path_service": self.path_service
            })
        ]