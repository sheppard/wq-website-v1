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
    html = _updateCode(html);
    return html;
}

function _updateCode(html) {
    if (!html.match('wq for Django')) {
        return html;
    }
    var rows = html.split('\n'),
        rowid = {};

    function sectionDone() {
        if (!('pypi_start' in rowid) || !('npm_end' in rowid)) {
            return;
        }
        if ('both_start' in rowid && !('both_end' in rowid)) {
            return;
        }
        var start = rowid['pypi_start'],
            end,
            pypi_head = rows[start],
            pypi_code = rows.slice(start + 1, rowid['pypi_end'] + 1),
            npm_head = rows[rowid['npm_start']],
            npm_code = rows.slice(rowid['npm_start'] + 1, rowid['npm_end'] + 1);
        if ('both_end' in rowid) {
            var both_code = rows.slice(rowid['both_start'], rowid['both_end']);
            both_code[0] = both_code[0].split('>').slice(2).join('>');
            both_code.unshift('');
            var pypi_code_end = pypi_code[pypi_code.length - 1];
            pypi_code = pypi_code.slice(
                0, pypi_code.length - 1
            ).concat(both_code);
            if (pypi_code.join('\n').match(/define\(/)) {
                pypi_code.push('\n});');
            }
            pypi_code.push(pypi_code_end);
            npm_code = npm_code.slice(
                0, npm_code.length - 1
            ).concat(both_code).concat([npm_code[npm_code.length - 1]]);
            end = rowid['both_end'];
        } else {
            end = rowid['npm_end'];
        }
        for (var i = start; i < end; i++) {
            rows[i] = '';
        }
        rows[start] = pypi_head;
        rows[start + 1] = npm_head;
        rows[start + 2] = pypi_code.join('\n');
        rows[start + 3] = npm_code.join('\n');

        function setClass(row, class_name) {
            rows[start + row] = rows[start + row].replace(/>/, ' class="' + class_name + '">');
        }
        setClass(0, 'code-tab active pypi')
        setClass(1, 'code-tab npm')
        setClass(2, 'code-example active pypi')
        setClass(3, 'code-example npm')
        rowid = {};
    }
            
    function updateRow(row, i) {
        if (row.match('wq for Django')) {
            rowid['pypi_start'] = i
        } else if (row.match('wq for Node')){
            rowid['npm_start'] = i
        } else if (row.match('<pre>')) {
            if ('npm_start' in rowid && i > rowid['npm_start'] + 1) {
                console.log("HAS BOTH");
                rowid['both_start'] = i
            }
        } else if (row.match('</pre>')) {
            if ('both_start' in rowid) {
                rowid['both_end'] = i
            } else if ('npm_start' in rowid) {
                rowid['npm_end'] = i
            } else if ('pypi_start' in rowid) {
                rowid['pypi_end'] = i
            }
       } else if (row) {
            sectionDone()
       }
    }

    for (var i = 0; i < rows.length; i++) {
        updateRow(rows[i], i)
    }

    return rows.join('\n');
}

function _highlight() {
    $('pre code:not(.hljs)').each(function(i, el) {
        highlight.highlightBlock(el);
    });
}

});
