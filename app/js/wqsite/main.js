define(["wq/app", "wq/map", "wq/photos", "wq/router", "wq/markdown",
        "./config", "./doc", "./example", "highlight"],
function(app, map, photos, router, md, config, doc, example, highlight) {

var latest_version = null, versions = [];

// Initialize wq.app
app.use(map);
app.use(photos);
app.use(example);

app.init(config).then(function() {
    md.init();
    md.postProcess = _postProcess;
    doc.init();
    router.register('<slug>/docs/<slug>', _renderDoc);
    router.register('<slug>/docs/', _renderDoc);
    router.addRoute('.*.*', 's', _highlight);
    app.jqmInit();
    app.prefetchAll();

    var projectFilter = app.models.project.filterPage;
    app.models.project.filterPage = function(filter) {
        if (filter._) {
            delete filter._;
        }
        return projectFilter(filter);
    }
    app.models.markdowntype.load().then(function(data) {
        versions = [];
        data.list.forEach(function(v) {
            if (v.deprecated) {
                return;
            }
            if (v.current) {
                latest_version = v;
            }
            delete v.id;
            versions.push(v);
        });
        config.menu[0].id = latest_version.name + '/' + config.menu[0].id;
    });
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

function _postProcess(html) {
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
        ['app', 'db', 'io'].forEach(function(mod) {
            var url = "https://github.com/wq/wq." + mod + "/blob/";
            var re = new RegExp(url + "master", 'g');
            html = html.replace(re, url + latest_version[mod + '_branch']);
        });
        html = html.replace(
            /http[s]?:\/\/wq.io\/docs/g,
            "https://wq.io/" + latest_version.name + "/docs"
        );
    }
    return html;
}

function _highlight() {
    $('pre code:not(.hljs)').each(function(i, el) {
        highlight.highlightBlock(el);
    });
}

});
