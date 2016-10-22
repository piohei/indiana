import {Camera} from "./3d/camera"
import {Light} from "./3d/light"
import {Controls} from "./../utils/controls"

export class Scene {
  constructor(map) {
    this.map = map;
    this.renderer = _generateRenderer();
    this.camera = _generateCamera();
    this.light = _generateLight();
    this.controls = _generateControls(this.camera);

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
    this.controls.run(function() { _render(scene) })

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

function _generateCamera() {
  return new Camera();
}

function _generateLight() {
  return new Light();
}

function _generateControls(camera) {
  return new Controls(camera);
}

function _genreateScene(map, light) {
  var res = new THREE.Scene();

  res.add(light.getDirectional());
  res.add(light.getAmbient());

  res.add(map.getLocator().getMesh());

  var levels = map.getLevels();
  for(const level in levels) {
    res.add(levels[level].getFloor().getMesh());

    for(const wall of levels[level].getWalls()) {
      res.add(wall.getMesh());
    }

    for(const router of levels[level].getRouters()) {
      res.add(router.getMesh());
    }
  }

  return res;
}

function _onWindowResize(scene) {
  scene.getCamera().setAspect(window.innerWidth / window.innerHeight);
  scene.getCamera().updateProjectionMatrix();

  scene.getRenderer().setSize(window.innerWidth, window.innerHeight);
  scene.getControls().handleResize();

  _render(scene);
}

function _animate(scene) {
  requestAnimationFrame(function() { _animate(scene) });
  scene.getControls().update();
  _render(scene);
}

function _render(scene) {
  scene.getRenderer().render(scene.getScene(), scene.getCamera().getCamera());
}
