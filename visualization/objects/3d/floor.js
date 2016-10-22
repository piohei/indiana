export class Floor {
  constructor(vertices, color="#3800aa") {
    this.mesh = _generateMesh(vertices, color);
  }

  getMesh() {
    return this.mesh;
  }
}

// Theese are class private functions
function _generateGeometry(vertices) {
  var floorShape = new THREE.Shape();

  floorShape.moveTo(
      vertices[vertices.length - 1].x,
      vertices[vertices.length - 1].y
  );

  vertices.forEach(function(vertex) {
      floorShape.lineTo(vertex.x, vertex.y);
  });

  return floorShape.extrude({
    amount: 0.02,
    bevelEnabled: false
  }).rotateX( Math.PI / 2);
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
      color: color,
      emissive: color,
  });
}

function _generateMesh(vertices, color) {
  var geometry = _generateGeometry(vertices);
  var material = _generateMaterial(color);

  return new THREE.Mesh(geometry, material);
}
