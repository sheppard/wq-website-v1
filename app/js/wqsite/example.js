define(['jquery', 'jquery.mobile'], function($, jqm) {

return {
    'name': 'examples',
    'init': function() {},
    'run': function() {
        jqm.activePage.find('.ui-popup').on('popupbeforeposition', function() {
            var height = $(window).height() - 60;
            $(this).find('img').css('max-height', height + "px");
        });
    }
};

});
