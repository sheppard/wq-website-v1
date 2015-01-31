define(["wq/app", "wq/map", "wq/store", "wq/markdown", "wq/template",
        "./config", "./templates", "./doc"],
function(app, map, ds, md, tmpl, config, templates, doc) {

// Initialize wq.app
app.init(config, templates);
map.init(config.map);
md.init();
md.postProcess = function(html) {
    return html.replace(
        /(<\/h1>\s*<p><a) (href="https:\/\/github.com\/[^"]+\/blob)/,
        '$1 class="github-file" $2'
    ).replace(
        /a (href="https:\/\/github.com\/[^"]+\/blob)/g,
        'a class="github-src" $1'
    ).replace (
        /(href="http[s]?:\/\/(?!wq.io))/g,
        'rel="external" $1'
    );
}
doc.init();
app.jqmInit();

// Prefetch important data
['', 'research', 'identifiers', 'relationships', 'examples', 'chapters', 'docs'].forEach(prefetch);
function prefetch(url) {
    ds.prefetch({'url': url});
}

});
