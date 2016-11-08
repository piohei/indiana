export class Locator extends THREE.Mesh {
  constructor(color="#ff0000") {
    var geometry = _generateGeometry();
    var material = _generateMaterial(color);

    super(geometry, material);
  }

  setPosition(x=0, y=0, z=0) {
    this.position.x = x;
    this.position.y = -y;
  }
}

// Theese are class private functions
function _generateGeometry() {
  // locator is 1.8 height
  var headGeometry = new THREE.CircleGeometry(0.2, 32);

  headGeometry.translate(0, 0, 0.2);

  return headGeometry;
}

function _generateMaterial(color) {
  return new THREE.MeshBasicMaterial({
      color: color
  });
}
