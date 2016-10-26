export class Controls extends THREE.OrthographicTrackballControls {
  constructor(camera) {
    super(camera);

    this.noZoom = false;
    this.noPan = false;
    this.noRotate = true;
    this.noRoll = true;

    this.target = new THREE.Vector3(16.5, -6, 0);
  }

  run(render) {
    this.addEventListener('change', render);
  }
}
