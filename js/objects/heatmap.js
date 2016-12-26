import {HeatmapLevel} from './heatmap_level'

export class Heatmap {
  constructor(map) {
    this.levels = _generateHeatmapLevels(map);
  }

  getLevels() {
    return this.levels;
  }
}

// Theese are class private functions
function _generateHeatmapLevels(map) {
  var levels = {};

  for(const level in map.levels) {
    levels[level] = new HeatmapLevel(map.levels[level]);
  }

  return levels;
}
