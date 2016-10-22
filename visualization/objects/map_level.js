import {Floor} from './3d/floor'
import {Wall} from './3d/wall'
import {Router} from './3d/router'

export class MapLevel {
  constructor(level) {
    this.floor   = _generateFloor(level.floor);
    this.walls   = _generateWalls(level.walls);
    this.routers = _generateRouters(level.routers);
  }

  getFloor() {
    return this.floor;
  }

  getWalls() {
    return this.walls;
  }

  getRouters() {
    return this.routers;
  }
}

// Theese are class private functions
function _generateFloor(floor) {
  return new Floor(floor);
}

function _generateWalls(walls) {
  var res = [];
  for(const wall of walls) {
    res.push(new Wall(wall));
  }
  return res;
}

function _generateRouters(routers) {
  var res = [];
  for(const router of routers) {
    res.push(new Router(router));
  }
  return res;
}
