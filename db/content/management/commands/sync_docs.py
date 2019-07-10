from django.core.management.base import NoArgsCommand

from content.models import Doc, Chapter, MarkdownType
from django.conf import settings
from wq.app.build import collect

import yaml
import subprocess
from io import StringIO

import os
import re
import datetime


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        os.chdir(settings.DOCS_ROOT)
        subprocess.call(['git', 'fetch', '--tags'])
        os.chdir('../wq')
        for module in ('app', 'db', 'io'):
            os.chdir(module)
            subprocess.call(['git', 'fetch', '--tags'])
            os.chdir('..')

        os.chdir(settings.DOCS_ROOT)
        for i, version in enumerate(MarkdownType.objects.all()):
            subprocess.call(['git', 'checkout', version.doc_branch])
            if not version.doc_branch.startswith('v'):
                subprocess.call(['git', 'pull'])

            os.chdir('../wq');
            for module in ('app', 'db', 'io'):
                os.chdir(module)
                tag = getattr(version, module + '_branch')
                subprocess.call(['git', 'checkout', tag])
                if not version.doc_branch.startswith('v'):
                    subprocess.call(['git', 'pull'])
                os.chdir('..')

            self.update_docs(version)


    def update_docs(self, version):
        print("Version %s%s" % (version, " (current)" if version.current else ""))
        for i, c in enumerate(settings.CONF['docs']):
            chapter = Chapter(
                id=c['id'],
                title=c['label'],
                order=i,
            )
            chapter.save()

            docs = get_chapter_docs(c['id'])
            for j, d in enumerate(docs):
                doc = Doc.objects.find(d['id'])
                markdown, is_new = doc.markdown.get_or_create(
                    type=version
                )
                markdown.markdown = d['markdown']
                markdown.summary = d.get('description', '')
                markdown.save()

                if not version.current:
                    continue

                ident = doc.primary_identifier
                ident.slug = d['id']
                ident.save()
                doc.title = d['title']
                doc.chapter_id = d['chapter']
                doc.description = d.get('description', "")
                doc.image = d.get('image', None)
                doc.is_jsdoc = d.get('is_jsdoc', False)
                doc.interactive = d['interactive']
                doc.indent = d.get('indent', False)
                doc.removed = d.get('deprecated', False)
                doc.updated = d['updated']
                doc._order = d.get('order', j)
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
        parts = pipe.stdout.read().decode('utf-8').split(" ")
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

        if 'title' not in doc:
            doc['title'] = re.match('(.*)', markdown).group(0)
        if 'description' not in doc:
            match = re.search(r'\n(.+?\.)\s', markdown)
            if match:
                desc = match.group(1)
                desc = desc.replace('[', '')
                desc = desc.replace(']', '')
                desc = desc.replace('*', '')
                desc = desc.replace('`', '')
                doc['description'] = desc
        if 'image' not in doc:
            match = re.search(r"wq.io/(.+?)\.png", markdown)
            if match:
                doc['image'] = "/%s.png" % match.group(1)

        doc['markdown'] = markdown
        doc['interactive'] = "data-interactive" in markdown

        docs.append(doc)

    return docs
