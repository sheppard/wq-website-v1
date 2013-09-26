require(["wq/app", "wq/store", "wq/markdown", "config", "templates", "doc"],
function(app, ds, md, config, templates, doc) {

// Initialize wq.app
app.init(config, templates);
md.init();
doc.init();

// Prefetch important data
['', 'research', 'identifiers', 'relationships'].forEach(prefetch);
function prefetch(url) {
    ds.prefetch({'url': url});
}

});
