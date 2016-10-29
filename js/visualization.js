import {Map} from './objects/map'
import {Scene} from './scene/scene'
import {WindowedScene} from './scene/windowed_scene'

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
