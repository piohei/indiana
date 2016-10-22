import {Map} from './objects/map'
import {Scene} from './scene/scene'

window.run = function() {
  $.getJSON("/map").done(function (map) {
    var map = new Map(map);
    var scene = new Scene(map);
    scene.show();
  }).fail(function (data) {
    alert("Error while getting map!");
  });
};
