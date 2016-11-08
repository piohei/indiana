export class Wall extends THREE.Line {
  constructor(vertices, height=2.5, color="#000000") {
    var geometry = _generateGeometry(vertices, height);
    var material = _generateMaterial(color);

    super(geometry, material);
  }
}

// Theese are class private functions
function _generateGeometry(vertices, height) {
  var from = vertices[0];
  var to   = vertices[1];

  var geometry = new THREE.Geometry();
  geometry.vertices.push(
    new THREE.Vector3(from.x, -1 * from.y, 0),
    new THREE.Vector3(to.x, -1 * to.y, 0)
  );

  return geometry;
}

function _generateMaterial(color) {
  return new THREE.LineBasicMaterial({
    color: color,
    linewidth: 1
  });
}
