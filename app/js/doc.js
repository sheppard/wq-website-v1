define(["wq/pages", "docs", "config"],
function(pages, docs, config) {

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
        _docs[id] = {
            'id': id,
            'type_id': type.id,
            'type_label': type.label,
            'label': label,
            'markdown': doc
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
    if (_docs[id])
        pages.go('docs/' + id, 'doc_detail', _docs[id], ui);
    else
        pages.notFound('docs/' + id);
}

// Initialize URL routes
function init() {
    pages.register('docs/', _renderList);
    pages.register('docs/(.+)', _renderItem);
}

return {
    'init': init
}

});
