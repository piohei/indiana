import {ReportMapLevel} from './report_map_level'

export class ReportMap {
  constructor(map) {
    this.levels = _generateReportLevels(map);
  }

  getLevels() {
    return this.levels;
  }
}

// Theese are class private functions
function _generateReportLevels(map) {
  var levels = {};

  for(const level in map.levels) {
    levels[level] = new ReportMapLevel(map.levels[level]);
  }

  return levels;
}
