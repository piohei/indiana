export class Floor extends THREE.Mesh {
  constructor(vertices, color="#3800aa") {
    var geometry = _generateGeometry(vertices);
    var material = _generateMaterial(color);

    super(geometry, material);
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
