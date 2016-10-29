export class Light {
  constructor(color="#ffffff", intensity=0.4) {
    this.directional = _generateDirectional(color, intensity);
    this.ambient     = _generateAmbient(color, intensity);
  }

  getDirectional() {
    return this.directional;
  }

  getAmbient() {
    return this.ambient;
  }
}

// Theese are class private functions
function _generateDirectional(color, intensity) {
  var light = new THREE.DirectionalLight(color, intensity);
  light.position.set(0.0, 0.0, 10.0).normalize();
  return light;
}

function _generateAmbient(color, intensity) {
  return new THREE.AmbientLight(color, intensity);
}
