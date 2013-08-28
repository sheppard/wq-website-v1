require(["wq/app", "wq/store", "config", "templates", "doc"],
function(app, ds, config, templates, doc) {

// Initialize wq.app
app.init(config, templates);
doc.init();

// Prefetch important data
['', 'research', 'identifiers', 'relationships'].forEach(prefetch);
function prefetch(url) {
    ds.prefetch({'url': url});
}

});
