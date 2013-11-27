requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'wqsite': '../wqsite',
        'docs': '../docs',
        'db': '../../'
    }
});

requirejs(['wqsite/main']);
