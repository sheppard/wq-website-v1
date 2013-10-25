define(["wq/lib/jquery.mobile", "wq/pages", "docs", "config"],
function(jqm, pages, docs, config) {

var _docs = {}; // Docs by id
var _list = []; // Docs sorted by section, then title

// Combine documentation markdown files into a single sorted array
config.docs.forEach(function(type) {
    var items = [];

    // Section header
    _list.push({
        'id': type.id,
        'type_id': type.id,
        'label': type.label,
        'section': true
    });

    // Documentation pages for this section
    for (var id in docs[type.id]) {
        var doc = docs[type.id][id];
        var label = doc.substring(0, doc.indexOf("\n"));
        var interactive = doc.indexOf("data-interactive") > -1;
        var is_jsdoc = false;
        if (id.indexOf(".js") > 1) {
            // Googlebot doesn't like webpage URLs ending with .js
            id = id.replace(".js", "-js");
            is_jsdoc = true;
        }
        _docs[id] = {
            'id': id,
            'is_jsdoc': is_jsdoc,
            'type_id': type.id,
            'type_label': type.label,
            'label': label,
            'markdown': doc,
            'interactive': interactive
        };
        items.push(_docs[id]);
    };
    // Sort alphabetically
    items.sort(function(a, b){ 
        if (a.id < b.id) return -1;
        if (a.id > b.id) return 1;
        return 0;
    });
    _list = _list.concat(items);
});

// Mimic wq/app.js _renderList
function _renderList(match, ui, params) {
    var list = _list;
    var url = 'docs/';
    if (params && params.section) {
        list = list.filter(function(d){
            return d.type_id == params.section;
        });
        url += '?section=' + params.section;
    }
    pages.go(url, 'doc_list', {'list': list}, ui);
}

// Mimic wq/app.js _renderItem
function _renderItem(match, ui, params) {
    var id = match[1];
    if (id.indexOf('.js') > -1)
        id = id.replace('.js', '-js');
    if (_docs[id])
        pages.go('docs/' + id, 'doc_detail', _docs[id], ui);
    else
        pages.notFound('docs/' + id);
}

// Custom scripting for doc pages
function _showItem(match, ui, params, hash, evt, $page) {
    _loadInteraction(match[1], $page);
}

function _loadInteraction(docid, $page) {
    var info = _docs[docid];
    if (!info || !info.interactive)
        return;

    // Automatically load and execute custom script for this doc
    var modname = info.id;
    if (info.is_jsdoc)
        modname = modname.replace("-js", ".js");
    require(['docs/' + info.type_id + '/' + modname + '-ui'], 
        function(script) {
            var $elems = $page.find('[data-interactive]');
            script($elems);
        }
    );
}

// Initialize URL routes
function init() {
    pages.register('docs/', _renderList);
    pages.register('docs/(.+)', _renderItem);
    pages.addRoute('docs/(.+)','s', _showItem);

    // Ensure interaction loads when doc is rendered on server via deep link
    var $page = jqm.activePage;
    if ($page && $page.data('docid')) {
        _loadInteraction($page.data('docid'), $page);
    }
}

return {
    'init': init
}

});
