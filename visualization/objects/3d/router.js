export class Router {
  constructor(position, height=2.5, color="#239123") {
    this.mesh = _generateMesh(position, height, color);
  }

  getMesh() {
    return this.mesh;
  }
}

// Theese are class private functions
function _generateGeometry(position, height) {
  var geometry = new THREE.SphereGeometry(0.1, 16, 16);
  geometry.translate(position.x, height - 0.1, position.y);
  return geometry;
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
      color: color,
      emissive: color,
  });
}

function _generateMesh(position, height, color) {
  var geometry = _generateGeometry(position, height);
  var material = _generateMaterial(color);

  return new THREE.Mesh(geometry, material);
}
