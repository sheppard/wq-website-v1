define(["wq/app", "wq/map", "wq/pages", "wq/store", "wq/markdown", "wq/template",
        "./config", "data/templates", "./doc", "./example"],
function(app, map, pages, ds, md, tmpl, config, templates, doc, example) {

// Initialize wq.app
app.init(config, templates);
map.init(config.map);
md.init();
md.postProcess = function(html) {
    html = html.replace(
        /(<\/h1>\s*<p><a) (href="https:\/\/github.com\/[^"]+\/blob)/,
        '$1 class="github-file" $2'
    ).replace(
        /a (href="https:\/\/github.com\/[^"]+\/blob)/g,
        'a class="github-src" $1'
    ).replace (
        /(href="http[s]?:\/\/(?!wq.io))/g,
        'rel="external" $1'
    );
    if (latest_version) {
        html = html.replace(
            /(https:\/\/github.com\/[^"]+\/blob\/)master/g,
            "$1" + latest_version.branch
        );
        html = html.replace(
            /http[s]?:\/\/wq.io\/docs/g,
            "https://wq.io/" + latest_version.name + "/docs"
        );
    }
    return html;
}
doc.init();
example.init();
pages.register('<slug>/docs/<slug>', _renderDoc);
pages.register('<slug>/docs/', _renderDoc);
app.jqmInit();

// Prefetch important data
['', 'research', 'identifiers', 'relationships', 'examples', 'chapters',
 'docs', 'markdown', 'versions'].forEach(prefetch);
function prefetch(url) {
    ds.prefetch({'url': url});
}

var latest_version = null, versions = [];
ds.getList({'url': 'versions'}, function(list) {
    versions = [];
    list.forEach(function(v) {
        versions.push({
            'name': v.name,
            'title': v.title,
            'branch': v.branch
        });
    });
    latest_version = versions[versions.length - 1];
    latest_version.current = true;
    config.menu[2].id = latest_version.name + '/' + config.menu[2].id;
});

function _renderDoc(match, ui, params) {
    if (match[1] == latest_version.name) {
        // Latest version docs are always cached locally
        var url = match[0].replace(/^\//, "").split('?')[0];
        var context = {
            'doc_version': latest_version.name,
        };
        if (!match[2]) {
            context['versions'] = versions;
        }
        app.go('doc', ui, params, match[2] || false, false, url, context);
    } else {
        // All other versions are rendered on server
        var options = ui.options || {};
        options.wqSkip = true;
        console.log(match[0])
        $.mobile.changePage(match[0], options);
    }
}

});
