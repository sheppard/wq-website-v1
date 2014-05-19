from django.conf import settings

ALIAS = {
    "docs": "chapters"
}

def menu(request):
    result = []
    for item in settings.CONF['menu']:
        item = item.copy()
        slug = request.path.split("/")[1]
        ids = [item['id'].split("/")[0]]
        if ids[0] in ALIAS:
           ids.append(ALIAS[ids[0]])

        if slug in ids:
            item['current'] = True
        result.append(item)
    return {'menu': result}
