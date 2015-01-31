define(["./conf", "db/config", "./render"],
function(config, dbconfig, render) {

// Template renderer defaults
config.defaults = {
    'menu': config.menu,
    'current': render.current
};

// jQM transitions
config.transitions = {
    'default': "none",
    'maxwidth': 800
};

// Map defaults
config.map = {
    'zoom': 10,
    'center': [44.98, -93.3]
};

// wq.db configuration 
for (var name in dbconfig)
    config[name] = dbconfig[name];

return config;
});
