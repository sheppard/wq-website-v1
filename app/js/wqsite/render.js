// Context helpers
define(["wq/pages"],
function(pages) {
return {
    'current': function() {
        // Selected menu page
        return pages.info.path.indexOf(this.id) == 0;
    }
};
});
