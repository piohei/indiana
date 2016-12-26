import {Map} from './objects/map'
import {Scene} from './scene/scene'
import {Fingerprint} from './fingerprint/fingerprint'
import {Path} from './path/path'
import {PositionUpdater} from './updaters/position'
import {Benchmark} from './benchmark/benchmark'
import {Reports} from './reports/reports'

window.currentPositions = {};

window.run = function(type, elementId=null, enableControls=true, zoom=1.0) {
  var url;
  
  if(type === 'report') {
    var report_num = window.location.pathname.split("/");
    report_num = report_num[report_num.length - 1];
    url = "/api/report_map/" + report_num;
  } else {
    url = "/api/map";
  }

  $.getJSON(url).done(function (map) {
    var scene = new Scene(type, map, elementId, enableControls, zoom);
    scene.show();
  }).fail(function () {
    alert("Error while getting map!");
  });
};

window.fingerprint = new Fingerprint(
  window.location.hostname,
  8888,
  "fingerprint"
);

window.benchmark = new Benchmark(
    window.location.hostname,
    8888,
    "benchmark"
);

window.path = new Path(
  window.location.hostname,
  8888,
  "path"
);

window.positionUpdater = new PositionUpdater(
  window.location.hostname,
  8888
);

window.reports = new Reports();
