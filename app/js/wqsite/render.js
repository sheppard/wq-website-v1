// Context helpers
define(["wq/router"],
function(router) {
var ALIAS = {
   'docs/': 'chapters/'
};
return {
    'current': function() {
        // Selected menu page
        var path = router.info.path;
        return ( path.indexOf(this.id) == 0 || path.indexOf(ALIAS[this.id]) == 0);
    }
};
});
