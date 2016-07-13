define(["data/conf", "data/config", "data/templates", "./render"],
function(config, dbconfig, templates, render) {

// Template renderer configuration
config.template = {
    'templates': templates,
    'partials': templates.partials,
    'defaults': {
        'menu': config.menu,
        'current': render.current
    }
};

// jQM transitions
config.transitions = {
    'default': "none",
    'maxwidth': 800
};


// Attribution (https://gist.github.com/mourner/1804938)
var attrib = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
var mapbox = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';

// Map defaults
config.map = {
    'bounds': [
        [44.78, -93.1],
        [45.18, -93.5]
    ],
    'basemaps': [{
        'name': 'MapBox Streets',
        'type': 'tile',
        'url': mapbox,
        'id': 'mapbox.streets',
        'accessToken': dbconfig.mapbox_token,
        'attribution': attrib
    }, {
        'name': 'MapBox Satellite',
        'type': 'tile',
        'url': mapbox,
        'id': 'mapbox.satellite',
        'accessToken': dbconfig.mapbox_token,
        'attribution': attrib
    }]
};

// wq.db configuration 
for (var name in dbconfig)
    config[name] = dbconfig[name];

return config;
});
