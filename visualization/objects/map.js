import {MapLevel} from './map_level'
import {Locator} from './3d/locator'

export class Map {
  constructor(map) {
    this.levels = _generateLevels(map);
    this.locator = _genreateLocator();
  }

  getLevels() {
    return this.levels;
  }

  getLocator() {
    return this.locator;
  }
}

// Theese are class private functions
function _generateLevels(map) {
  var levels = {}

  for(const level in map.levels) {
    levels[level] = new MapLevel(map.levels[level]);
  }

  return levels;
}

function _genreateLocator() {
  return new Locator();
}
