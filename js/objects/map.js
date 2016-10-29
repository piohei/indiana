import {MapLevel} from './map_level'

import {Locator as Locator2D} from './2d/locator'

import {Locator as Locator3D} from './3d/locator'

export class Map {
  constructor(type, map) {
    this.type = type;
    this.levels = _generateLevels(type, map);
    this.locator = _genreateLocator(type);
  }

  getLevels() {
    return this.levels;
  }

  getLocator() {
    return this.locator;
  }
}

// Theese are class private functions
function _generateLevels(type, map) {
  var levels = {}

  for(const level in map.levels) {
    levels[level] = new MapLevel(type, map.levels[level]);
  }

  return levels;
}

function _genreateLocator(type) {
  switch(type) {
    case '2d':
      return new Locator2D();
    case '3d':
      return new Locator3D();
  }
}
