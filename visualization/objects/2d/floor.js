export class Floor extends THREE.Mesh {
  constructor(vertices, color="#ffffff") {
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
      floorShape.lineTo(vertex.x, -1 * vertex.y);
  });

  var geometry = new THREE.ShapeGeometry(floorShape)
  geometry.translate(0, 0, -0.1);

  return geometry;
}

function _generateMaterial(color) {
  return new THREE.MeshBasicMaterial({
      color: color,
  });
}
