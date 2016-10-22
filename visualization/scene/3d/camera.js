export class Camera {
  constructor() {
    this.camera = _generateCamera();
  }

  getCamera() {
    return this.camera;
  }

  setAspect(aspect) {
    this.camera.aspect = aspect;
  }

  updateProjectionMatrix() {
    this.camera.updateProjectionMatrix();
  }
}

// Theese are class private functions
function _generateCamera() {
  var camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    1,
    2000
  );

  camera.position.x = 20;
  camera.position.y = 10;
  camera.position.z = 20;

  camera.rotation.x = 0;
  camera.rotation.y = 0;
  camera.rotation.z = 0;

  return camera
}
