import {FloorPolygon} from './floorPolygon'

export class Floor {

    constructor(floor_data) {
        this.polygons = floor_data.map(polygon_data => new FloorPolygon(polygon_data.polygon, polygon_data.color))
    }

    getPolygons() {
        return this.polygons
    }
}