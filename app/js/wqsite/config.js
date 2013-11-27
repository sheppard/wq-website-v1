define(["./conf", "db/config", "./render"],
function(config, dbconfig, render) {

// Template renderer defaults
config.defaults = {
    'menu': config.menu,
    'current': render.current
}

// jQM transitions
config.transitions = {
    'default': "fade",
    'maxwidth': 800
}

// wq.db configuration 
for (var name in dbconfig)
    config[name] = dbconfig[name];

return config;
});
