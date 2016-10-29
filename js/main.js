import {Map} from './objects/map'
import {Scene} from './scene/scene'
import {Fingertip} from './fingertip/fingertip'
import {Path} from './path/path'
import {PositionUpdater} from './updaters/position'

window.currentPosition = {
  x: 0, y: 0, z: 0
};

window.run = function(type, elementId=null, enableControls=true) {
  $.getJSON("/map").done(function (map) {
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
)

window.positionUpdater = new PositionUpdater(
  window.location.hostname,
  8888,
  "99:AF:00:12:12:12"
)
