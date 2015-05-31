requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'wqsite': '../wqsite',
        'docs': '../docs',
        'data': '../data'
    }
});

requirejs(['wqsite/main']);
