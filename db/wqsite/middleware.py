class DocVersionMiddleware:
    def process_request(self, request):
        version = request.path.split('/')[1]
        if version.split('.')[0].isdigit():
            request.doc_version = version
