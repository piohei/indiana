import {Camera as Camera2D} from "./2d/camera"
import {Controls as Controls2D} from "./../utils/2d/controls"

import {Camera as Camera3D} from "./3d/camera"
import {Controls as Controls3D} from "./../utils/3d/controls"
import {Light as Light3D} from "./3d/light"

import {Map} from "./../objects/map"

export class Scene {
  constructor(type, map) {
    this.map = _generateMap(type, map);
    this.renderer = _generateRenderer();
    this.camera = _generateCamera(type);
    this.light = _generateLight(type);
    this.controls = _generateControls(type, this.camera);

    // This must be initalized last
    this.scene = _genreateScene(this.map, this.light);
  }

  getMap() {
    return this.map;
  }

  getRenderer() {
    return this.renderer;
  }

  getCamera() {
    return this.camera;
  }

  getLight() {
    return this.light;
  }

  getControls() {
    return this.controls;
  }

  getScene() {
    return this.scene;
  }

  show() {
    var scene = this;

    document.body.appendChild(this.renderer.domElement);
    window.addEventListener('resize', function() { _onWindowResize(scene) }, false);
    if(this.controls != null) {
      this.controls.run(function() { _render(scene) })
    }

    _animate(scene);
  }
}

// Theese are class private functions
function _generateRenderer() {
  var renderer = new THREE.WebGLRenderer();
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  return renderer;
}

function _generateMap(type, map) {
  return new Map(type, map);
}

function _generateCamera(type) {
  switch(type) {
    case '2d':
      return new Camera2D();
    case '3d':
      return new Camera3D();
  }
}

function _generateLight(type) {
  switch(type) {
    case '2d':
      return null;
    case '3d':
      return new Light3D();
  }
}

function _generateControls(type, camera) {
  switch(type) {
    case '2d':
      return new Controls2D(camera);
    case '3d':
      return new Controls3D(camera);
  }
}

function _genreateScene(map, light) {
  var res = new THREE.Scene();

  if(light != null) {
    res.add(light.getDirectional());
    res.add(light.getAmbient());
  }

  res.add(map.getLocator());

  var levels = map.getLevels();
  for(const level in levels) {
    res.add(levels[level].getFloor());

    for(const wall of levels[level].getWalls()) {
      res.add(wall);
    }

    for(const router of levels[level].getRouters()) {
      res.add(router);
    }
  }

  return res;
}

function _onWindowResize(scene) {
  scene.getCamera().aspect = window.innerWidth / window.innerHeight;
  scene.getCamera().updateProjectionMatrix();

  scene.getRenderer().setSize(window.innerWidth, window.innerHeight);
  if(scene.getControls() != null) {
    scene.getControls().handleResize();
  }

  _render(scene);
}

function _animate(scene) {
  requestAnimationFrame(function() { _animate(scene) });
  if(scene.getControls() != null) {
    scene.getControls().update();
  }
  _render(scene);
}

function _render(scene) {
  scene.getRenderer().render(scene.getScene(), scene.getCamera());
}
