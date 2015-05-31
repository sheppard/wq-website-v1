from django.conf import settings

ALIAS = {
    "docs": "chapters"
}


def menu(request):
    result = []
    doc_version = getattr(request, 'doc_version', None)
    slug = request.path.split("/")[2 if doc_version else 1]
    for item in settings.CONF['menu']:
        item = item.copy()
        ids = [item['id'].split("/")[0]]
        if ids[0] in ALIAS:
            ids.append(ALIAS[ids[0]])

        if slug in ids:
            item['current'] = True
        if doc_version and item['id'] == 'docs/':
            item['id'] = doc_version + '/' + item['id']

        result.append(item)
    return {'menu': result}
