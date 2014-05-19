define(["jquery.mobile", "wq/pages", "wq/store"],
function(jqm, pages, ds) {

// Custom scripting for doc pages
function _showItem(match, ui, params, hash, evt, $page) {
    _loadInteraction(match[1], $page);
}

function _loadInteraction(docid, $page) {
    ds.getList({'url': 'docs'}, function(list) {
        _execInteraction(list.find(docid), $page);
    });
}

function _execInteraction(info, $page) {
    if (!info || !info.interactive)
        return;

    // Automatically load and execute custom script for this doc
    var modname = info.id;
    if (info.is_jsdoc)
        modname = modname.replace("-js", ".js");
    require(['docs/' + info.chapter_id + '/' + modname + '-ui'], 
        function(script) {
            var $elems = $page.find('[data-interactive]');
            script($elems);
        }
    );
}

// Initialize URL routes
function init() {
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
