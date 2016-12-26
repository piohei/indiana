import {Camera as Camera2D} from "./2d/camera"
import {Controls as Controls2D} from "./../utils/2d/controls"

import {Camera as Camera3D} from "./3d/camera"
import {Controls as Controls3D} from "./../utils/3d/controls"
import {Light as Light3D} from "./3d/light"

import {Map} from "./../objects/map"
import {ReportMap} from "./../objects/report_map"
import {Heatmap} from "./../objects/heatmap"

export class Scene {
  constructor(type, map, elementId=null, enableControls=true, zoom=1.0) {
    this.elementId = elementId;
    this.map = _generateMap(type, map);
    this.renderer = _generateRenderer(elementId);
    this.camera = _generateCamera(type, elementId, zoom);
    this.light = _generateLight(type);
    if(enableControls) {
      this.controls = _generateControls(type, this.camera);
    } else {
      this.controls = null;
    }

    // This must be initalized last
    this.scene = _genreateScene(type, this.map, this.light);
  }

  setLocatorPosition(locatorName, position) {
    this.map.setLocatorPosition(locatorName, position, locator => this.scene.add(locator));
  }

  show(animate=true) {
    var closureCopy = this;

    if(this.elementId == null) {
      document.body.appendChild(this.renderer.domElement);
      window.addEventListener('resize', function() { closureCopy._onWindowResize() }, false);
    }

    if(this.controls != null) {
      this.controls.run(function() { closureCopy._render() })
    }

    if(animate) {
      this._animate();
    }
  }

  // Proteced functions
  _onWindowResize() {
    this.camera.updateWindowResize(window.innerWidth, window.innerHeight);

    this.renderer.setSize(window.innerWidth, window.innerHeight);
    if(this.controls != null) {
      this.controls.handleResize();
    }

    this._render();
  }

  _animate() {
    var closureCopy = this;
    if (window.stopAnimation) return;
    requestAnimationFrame(function() { closureCopy._animate() });
    Object.keys(window.currentPositions).forEach(locatorName => {
      this.setLocatorPosition(locatorName, window.currentPositions[locatorName])
    });

    if(this.controls != null) {
      this.controls.update();
    }

    this._render();
  }

  _render() {
    this.renderer.render(this.scene, this.camera);
  }
}

// Theese are class private functions
function _generateRenderer(elementId) {
  var renderer;

  if(elementId == null) {
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
  } else {
    renderer = new THREE.WebGLRenderer({
      canvas: document.getElementById(elementId)
    });
  }

  renderer.setPixelRatio(window.devicePixelRatio);
  return renderer;
}

function _generateMap(type, map) {
  switch(type) {
    case '2d':
      return new Map(type, map);
    case 'report':
      return new ReportMap(map);
    case 'heatmap':
      return new Heatmap(map);
    case '3d':
      return new Map(type, map);
  }
}

function _generateCamera(type, elementId, zoom=1.0) {
  var width  = window.innerWidth;
  var height = window.innerHeight;

  if(elementId != null) {
    width  = document.getElementById("map-canvas").width;
    height = document.getElementById("map-canvas").height;
  }

  switch(type) {
    case '2d':
      return new Camera2D(width, height, zoom);
    case 'report':
      return new Camera2D(width, height, zoom);
    case 'heatmap':
      return new Camera2D(width, height, zoom);
    case '3d':
      return new Camera3D(width, height, zoom);
  }
}

function _generateLight(type) {
  switch(type) {
    case '2d':
      return null;
    case 'report':
      return null;
    case 'heatmap':
      return null;
    case '3d':
      return new Light3D();
  }
}

function _generateControls(type, camera) {
  switch(type) {
    case '2d':
      return new Controls2D(camera);
    case 'report':
      return new Controls2D(camera);
    case 'heatmap':
      return new Controls2D(camera);
    case '3d':
      return new Controls3D(camera);
  }
}

function _genreateScene(type, map, light) {
  var res = new THREE.Scene();

  if(light != null) {
    res.add(light.getDirectional());
    res.add(light.getAmbient());
  }

  if(type !== 'report' && type != 'heatmap') {
    var locators = map.getLocators();
    Object.keys(locators).forEach(locatorName => {
      res.add(locators[locatorName]);
    });
  }

  var levels = map.getLevels();
  for(const level in levels) {
    if(type != 'heatmap') {
      res.add(levels[level].getFloor());
    } else {
      for (const polygon of levels[level].getFloor().getPolygons()) {
        res.add(polygon);
      }
    }

    for(const wall of levels[level].getWalls()) {
      res.add(wall);
    }

    for(const router of levels[level].getRouters()) {
      res.add(router);
    }

    if (type != 'heatmap') {
          for (const sample of levels[level].getSamples()) {
            res.add(sample);
              }
          }

    if(type === 'report') {
      for(const point of levels[level].getCalculatedPoints()) {
        res.add(point);
      }
    }
  }

  return res;
}
