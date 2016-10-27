export class Camera extends THREE.OrthographicCamera {
  constructor(width, height) {
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
  }
}
