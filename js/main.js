import {Map} from './objects/map'
import {Scene} from './scene/scene'
import {Fingertip} from './fingertip/fingertip'
import {Path} from './path/path'
import {PositionUpdater} from './updaters/position'

window.currentPositions = {};

window.run = function(type, elementId=null, enableControls=true) {
  var url;
  
  if(type === 'report') {
    var report_num = window.location.pathname.split("/");
    report_num = report_num[report_num.length - 1];
    url = "/report_map/" + report_num;
  } else {
    url = "/map";
  }

  $.getJSON(url).done(function (map) {
    var scene = new Scene(type, map, elementId, enableControls)
    scene.show();
  }).fail(function (data) {
    alert("Error while getting map!");
  });
};

window.fingertip = new Fingertip(
  window.location.hostname,
  8887,
  "fingertip"
);

window.path = new Path(
  window.location.hostname,
  8887,
  "path"
);

window.positionUpdater = new PositionUpdater(
  window.location.hostname,
  8888
);
