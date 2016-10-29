export class Router extends THREE.Mesh {
  constructor(position, height=2.5, color="#239123") {
    var geometry = _generateGeometry(position, height);
    var material = _generateMaterial(color);

    super(geometry, material);
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
