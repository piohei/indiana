export class Sample extends THREE.Mesh {
  constructor(position, height=0, color="#2760bc") {
    var geometry = _generateGeometry(position, height);
    var material = _generateMaterial(color);

    super(geometry, material);
  }
}

// Theese are class private functions
function _generateGeometry(position, height) {
  var geometry = new THREE.SphereGeometry(0.1, 16, 16);
  geometry.translate(position.x, height, position.y);
  return geometry;
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
    color: color,
    emissive: color
  });
}
