require(["wq/app", "wq/store", "wq/markdown", "config", "templates", "doc"],
function(app, ds, md, config, templates, doc) {

// Initialize wq.app
app.init(config, templates);
md.init();
md.postProcess = function(html) {
    return html.replace(
        /(<\/h1>\s*<p><a) (href="https:\/\/github.com\/[^"]+\/blob)/,
        '$1 class="github-file" $2'
    ).replace(
        /a (href="https:\/\/github.com\/[^"]+\/blob)/g,
        'a class="github-src" $1'
    ).replace (
        /(href="http[s]?:\/\/[^wq.io])/g,
        'rel="external" $1'
    );
}
doc.init();

// Prefetch important data
['', 'research', 'identifiers', 'relationships'].forEach(prefetch);
function prefetch(url) {
    ds.prefetch({'url': url});
}

});
