from django.core.management.base import NoArgsCommand

from content.models import Doc, Chapter
from django.conf import settings
from wq.app.build import collect

import yaml
import subprocess
from StringIO import StringIO

import os
import re
import datetime


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for i, c in enumerate(settings.CONF['docs']):
            chapter = Chapter(
                id=c['id'],
                title=c['label'],
                order=i,
            )
            chapter.save()

            docs = get_chapter_docs(c['id'])
            for i, d in enumerate(docs):
                doc = Doc.objects.find(d['id'])
                doc.title = d['title']
                doc.chapter_id = d['chapter']
                doc.description = d.get('description', "")
                doc.is_jsdoc = d.get('is_jsdoc', False)
                doc.interactive = d['interactive']
                doc.updated = d['updated']
                doc.markdown = d['markdown']
                doc._order = d.get('order', i)
                doc.save()


# Load documentation files from directory
def get_chapter_docs(chapter_id):
    doc_files = collect.readfiles(
        '%s/%s' % (settings.DOCS_ROOT, chapter_id),
        'md'
    )

    docs = []
    for id in sorted(doc_files.keys()):
        doc = {
            'id': id,
            'chapter': chapter_id,
        }

        # Extract modification timestamp from git log
        pipe = subprocess.Popen([
            "git", "log", "-1", "--format=%ai", "%s/%s.md" % (chapter_id, id)
        ], stdout=subprocess.PIPE, cwd=settings.DOCS_ROOT)

        # FIXME: handle time zone?
        parts = pipe.stdout.read().split(" ")
        doc['updated'] = datetime.datetime.strptime(
            parts[0] + " " + parts[1], "%Y-%m-%d %X"
        )

        # Googlebot doesn't like webpage URLs ending with .js
        if id.endswith('.js'):
            doc['id'] = id.replace('.js', '-js')
            doc['is_jsdoc'] = True

        markdown = doc_files[id]
        # Optional YAML front matter
        if markdown.startswith('---'):
            conf, markdown = markdown[3:].split("\n---\n")
            doc.update(yaml.load(conf))
            markdown = markdown[1:]

        doc['title'] = re.match('(.*)', markdown).group(0)
        doc['markdown'] = markdown
        doc['interactive'] = "data-interactive" in markdown

        docs.append(doc)

    return docs
