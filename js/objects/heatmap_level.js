import {Floor as Floor2D} from './2d/floor'
import {Wall as Wall2D} from './2d/wall'
import {Router as Router2D} from './2d/router'
import {Sample as Sample2D} from './2d/sample'
import {CalculatedPoint as CalculatedPoint2D} from './2d/calculated_point'

export class HeatmapLevel {
  constructor(level) {
    this.floor   = _generateReportFloor(level.floor);
    this.walls   = _generateReportWalls(level.walls);
    this.routers = _generateReportRouters(level.routers);
    this.cmap = level.cmap;
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

  getCmap() {
    return this.cmap;
  }
}

// Theese are class private functions
function _generateReportFloor(floor) {
  return new Floor2D(floor);
}

function _generateReportWall(wall) {
  return new Wall2D(wall);
}

function _generateReportRouter(router) {
  return new Router2D(router);
}

function _generateReportWalls(walls) {
  var res = [];
  for(const wall of walls) {
    res.push(_generateReportWall(wall));
  }
  return res;
}

function _generateReportRouters(routers) {
  var res = [];
  for(const router of routers) {
    res.push(_generateReportRouter(router));
  }
  return res;
}

