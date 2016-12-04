import {Floor as Floor2D} from './2d/floor'
import {Wall as Wall2D} from './2d/wall'
import {Router as Router2D} from './2d/router'
import {Sample as Sample2D} from './2d/sample'
import {CalculatedPoint as CalculatedPoint2D} from './2d/calculated_point'

export class ReportMapLevel {
  constructor(level) {
    this.floor   = _generateReportFloor(level.floor);
    this.walls   = _generateReportWalls(level.walls);
    this.routers = _generateReportRouters(level.routers);
    this.samples = _generateReportSamples(level.samples);
    this.calculated_points = _generateReportCalculatedPoints(level.calculated);
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

  getSamples() {
    return this.samples;
  }

  getCalculatedPoints() {
    return this.calculated_points;
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

function _generateReportSample(sample) {
  return new Sample2D(sample, 0, sample.color);
}

function _generateReportCalculatedPoint(point) {
  return new CalculatedPoint2D(point, 0, point.color);
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

function _generateReportSamples(samples) {
  var res = [];
  for(const sample of samples) {
    res.push(_generateReportSample(sample));
  }
  return res;
}

function _generateReportCalculatedPoints(calculated) {
  var res = [];
  for(const point of calculated) {
    res.push(_generateReportCalculatedPoint(point));
  }
  return res;
}

