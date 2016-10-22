export class Controls {
  constructor(camera) {
    this.controls = _generateControls(camera);
  }

  getControls() {
    return this.controls;
  }

  handleResize() {
    this.controls.handleResize();
  }

  update() {
    this.controls.update();
  }

  run(render) {
    this.controls.addEventListener('change', render);
  }
}

// Theese are class private functions
function _generateControls(camera) {
  return new THREE.OrbitControls(camera.getCamera());
}
