export class Controls extends THREE.OrbitControls {
  constructor(camera) {
    super(camera);
  }

  run(render) {
    this.addEventListener('change', render);
  }
}
