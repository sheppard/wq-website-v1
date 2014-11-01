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
['', 'research', 'identifiers', 'relationships', 'examples', 'chapters'].forEach(prefetch);
function prefetch(url) {
    ds.prefetch({'url': url});
}

if (ds.exists({'url': 'docs', 'page': 1}))
    _complete(ds.get({'url': 'docs', 'page': 1}));
ds.prefetch({'url': 'docs'}, _complete);

function _complete(data) {
    data = data.filter(function(d){
        return !d.section;
    });
    var completed = data.filter(function(d){
        return !d.incomplete;
    }).length;
    tmpl.setDefault(
        'completed',
        Math.round(completed / data.length * 100)
    );
}

});
