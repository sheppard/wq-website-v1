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
var osmAttr = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var aerialAttr = 'Imagery &copy; NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency';
var mqTilesAttr = 'Tiles &copy; <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="https://developer.mapquest.com/content/osm/mq_logo.png" />';

// Map defaults
config.map = {
    'bounds': [
        [44.78, -93.1],
        [45.18, -93.5]
    ],
    'basemaps': [{
        'name': 'Mapquest OSM',
        'type': 'tile',
        'url': 'https://otile{s}-s.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
        'subdomains': '1234',
        'attribution': osmAttr + ', ' + mqTilesAttr 
    }]
};

// wq.db configuration 
for (var name in dbconfig)
    config[name] = dbconfig[name];

return config;
});
