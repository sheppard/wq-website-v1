// Context helpers
define(["wq/pages"],
function(pages) {
var ALIAS = {
   'docs/': 'chapters/'
};
return {
    'current': function() {
        // Selected menu page
        var path = pages.info.path;
        return ( path.indexOf(this.id) == 0 || path.indexOf(ALIAS[this.id]) == 0);
    }
};
});
