export class Camera extends THREE.OrthographicCamera {
  constructor(width, height, zoom) {
    super(
      width / -2 / 30,
      width / 2 / 30,
      height / 2 / 30,
      height / -2 / 30,
      -500,
      1000
    );

    this.position.x = 16.5;
    this.position.y = -6;
    this.position.z = 10;

    this.rotation.x = 0;
    this.rotation.y = 0;
    this.rotation.z = 0;

    this.zoom = zoom;
    this.updateProjectionMatrix();
  }

  updateWindowResize(width, height) {
    this.left   = width / -2 / 30;
    this.right  = width / 2 / 30;
    this.top    = height / 2 / 30;
    this.bottom = height / -2 / 30;

    this.updateProjectionMatrix();
  }
}
