export class Camera extends THREE.PerspectiveCamera {
  constructor(width, height) {
    super(
      60,
      width / height,
      1,
      2000
    );

    this.position.x = 20;
    this.position.y = 10;
    this.position.z = 20;

    this.rotation.x = 0;
    this.rotation.y = 0;
    this.rotation.z = 0;
  }
}
