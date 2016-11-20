import {Floor as Floor2D} from './2d/floor'
import {Wall as Wall2D} from './2d/wall'
import {Router as Router2D} from './2d/router'
import {Sample as Sample2D} from './2d/sample'

import {Floor as Floor3D} from './3d/floor'
import {Wall as Wall3D} from './3d/wall'
import {Router as Router3D} from './3d/router'
import {Sample as Sample3D} from './3d/sample'

export class MapLevel {
  constructor(type, level) {
    this.floor   = _generateFloor(type, level.floor);
    this.walls   = _generateWalls(type, level.walls);
    this.routers = _generateRouters(type, level.routers);
    this.samples = _generateSamples(type, level.samples);
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
}

// Theese are class private functions
function _generateFloor(type, floor) {
  switch(type) {
    case '2d':
      return new Floor2D(floor);
    case '3d':
      return new Floor3D(floor);
  }
}

function _generateWall(type, wall) {
  switch(type) {
    case '2d':
      return new Wall2D(wall);
    case '3d':
      return new Wall3D(wall);
  }
}

function _generateRouter(type, router) {
  switch(type) {
    case '2d':
      return new Router2D(router);
    case '3d':
      return new Router3D(router);
  }
}

function _generateSample(type, sample) {
  switch(type) {
    case '2d':
      return new Sample2D(sample);
    case '3d':
      return new Sample3D(sample);
  }
}

function _generateWalls(type, walls) {
  var res = [];
  for(const wall of walls) {
    res.push(_generateWall(type, wall));
  }
  return res;
}

function _generateRouters(type, routers) {
  var res = [];
  for(const router of routers) {
    res.push(_generateRouter(type, router));
  }
  return res;
}

function _generateSamples(type, samples) {
  var res = [];
  for(const sample of samples) {
    res.push(_generateSample(type, sample));
  }
  return res;
}

