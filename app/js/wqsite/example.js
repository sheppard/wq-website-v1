define(['jquery', 'wq/pages'], function($, pages) {

function init() {
    pages.addRoute('examples/<slug>', 's', _showExample);
}

function _showExample(match, ui, params, hash, evt, $page) {
    $page.find('.ui-popup').on('popupbeforeposition', function() {
        var height = $(window).height() - 60;
        $(this).find('img').css('max-height', height + "px");
    });
};

return {
    'init': init
};

});
