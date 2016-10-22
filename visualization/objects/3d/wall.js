export class Wall {
  constructor(vertices, height=2.5, color="#5c018e") {
    this.mesh = _generateMesh(vertices, height, color);
  }

  getMesh() {
    return this.mesh;
  }
}

// Theese are class private functions
function _generateGeometry(vertices, height) {
  var from = vertices[0];
  var to   = vertices[1];

  var width = Math.sqrt(Math.pow(from.x - to.x, 2) + Math.pow(from.y - to.y, 2));
  var arc   = Math.atan2(from.y - to.y, to.x - from.x);

  return new THREE.PlaneGeometry(width, height).
    translate(width / 2, height / 2, 0).
    rotateY(arc).
    translate(from.x, 0, from.y);
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
      color: color,
      emissive: color,
      side: THREE.DoubleSide
  });
}

function _generateMesh(vertices, height, color) {
  var geometry = _generateGeometry(vertices, height);
  var material = _generateMaterial(color);

  return new THREE.Mesh(geometry, material);
}
