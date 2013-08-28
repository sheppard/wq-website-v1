from django.conf import settings

def menu(request):
    result = []
    for item in settings.CONF['menu']:
        item = item.copy()
        if request.path.startswith('/' + item['id']):
            item['current'] = True
        result.append(item)
    return {'menu': result}
