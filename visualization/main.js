import {Map} from './objects/map'
import {Scene} from './scene/scene'

window.run = function(type) {
  $.getJSON("/map").done(function (map) {
    var scene = new Scene(type, map);
    scene.show();
  }).fail(function (data) {
    alert("Error while getting map!");
  });
};
