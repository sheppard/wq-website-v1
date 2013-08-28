// Context helpers
define(["wq/pages", "wq/lib/marked"],
function(pages, marked) {
return {
    'current': function() {
        // Selected menu page
        return pages.info.path.indexOf(this.id) == 0;
    },
    'html': function() {
        // Render markdown from current context
        if (this.markdown)
            return marked.parse(this.markdown);
    }
};
});
