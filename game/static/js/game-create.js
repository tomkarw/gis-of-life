let vectorSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: function (extent) {
        return (
            'https://ahocevar.com/geoserver/wfs?service=WFS&' +
            'version=1.1.0&request=GetFeature&typename=osm:water_areas&' +
            'outputFormat=application/json&srsname=EPSG:3857&' +
            'bbox=' +
            extent.join(',') +
            ',EPSG:3857'
        );
    },
    strategy: ol.loadingstrategy.bbox,
});

let vector = new ol.layer.Vector({
    source: vectorSource,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'rgba(0, 0, 255, 1.0)',
            width: 2,
        }),
    }),
});

let key = 'yPkJGoOMurtiQZKcz87j';
let attributions =
    '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> ' +
    '<a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>';

let raster = new ol.layer.Tile({
    source: new ol.source.XYZ({
        attributions: attributions,
        url: 'https://api.maptiler.com/tiles/satellite/{z}/{x}/{y}.jpg?key=' + key,
        maxZoom: 20,
    }),
});

let map = new ol.Map({
    layers: [raster, vector],
    target: document.getElementById('map'),
    view: new ol.View({
        center: [-8908887.277395891, 5381918.072437216],
        maxZoom: 19,
        zoom: 12,
    }),
});

document.getElementById('create-button').addEventListener('click', function () {
    let coords = map.getView().getCenter();
    let zoom = map.getView().getZoom();
    let map_form = $('#map-form');
    map_form.append('coords', coords);
    map_form.append('zoom', zoom);
});
