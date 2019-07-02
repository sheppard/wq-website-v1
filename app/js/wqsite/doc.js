define(["jquery.mobile", "wq/router", "wq/app"],
function(jqm, router, app) {

var _codeTab = 'pypi';
// Custom scripting for doc pages
function _showItem(match, ui, params, hash, evt, $page) {
    _loadInteraction(match[2], $page);
    $page.find('.code-tab').click(function(evt) {
        if (evt.target.className.match(/npm/)) {
            _setCodeTab('npm', $page);
        } else {
            _setCodeTab('pypi', $page);
        }
    });
    _setCodeTab(_codeTab, $page);
}

function _loadInteraction(docid, $page) {
    app.models.doc.find(docid).then(function(doc) {
        _execInteraction(doc, $page);
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

function _setCodeTab(codeTab, $page) {
    _codeTab = codeTab;
    var $pypi = $page.find('.pypi'),
        $npm = $page.find('.npm');
    if (codeTab == 'pypi') {
        $pypi.addClass('active');
        $npm.removeClass('active');
    } else {
        $pypi.removeClass('active');
        $npm.addClass('active');
    }
}

// Initialize URL routes
function init() {
    router.addRoute('([^/]*)/docs/(.+)','s', _showItem);
}

return {
    'init': init
}

});
