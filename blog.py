from jinja2 import Environment, FileSystemLoader
from glob import glob
from markdown import markdown
from datetime import datetime
import shutil
import os
import cgi

class GhostWriter(object):
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates/'))
        self.env.globals['cgi'] = cgi

        # Removes static content and re copies it
        shutil.rmtree(os.path.join('output'))
        shutil.copytree(os.path.join('content', 'static'), os.path.join('output', 'static'))

        # Create empty entries
        self.entries = list()
        self.projects = list()

        # Run functions
        self.load(self.entries, 'entries')
        self.load(self.projects, 'projects')

        self.gen_page('content.html','')
        self.gen_pages('index.html', 'index.html', self.entries)
        self.gen_pages('feed.xml', 'feed.xml', self.entries)
        self.gen_pages('projects.html', 'projects.html', self.projects)

    # Loads all entries from 'content/entries'
    def load(self, stored, location):
        filenames = glob(os.path.join('content', location, '*'))
        for file in filenames:
            raw = open(file, 'r').read()
            title = None
            date = None
            tags = list()
            while True:
                if not raw or raw[0] != '#':
                    break
                line, raw = raw.split('\n', 1)
                item, rest = line[1:].split(' ', 1)
                if item == 'title':
                    title = rest
                if item == 'date':
                    date = rest
                if item == 'tags':
                    tags = rest.split(' ')

            stored.append(dict(
                link=date + "-" + title.replace(' ', '-').lower() + '.html',
                title=title,
                date=date,
                tags=tags,
                raw=raw,
                html=markdown(raw)
            ))

        stored.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)

    # Output all entries to 'output/posts'
    def gen_page(self, templateName, outputName):
        template = self.env.get_template(templateName)

        for entry in self.entries:
            output = template.render(entry=entry)

            with open(os.path.join('output', outputName, entry['link']), 'w') as f:
                f.write(output)

    def gen_pages(self, templateName, outputName, items):
        template = self.env.get_template(templateName)

        output = template.render(content=items)

        with open(os.path.join('output', outputName), 'w') as f:
            f.write(output)


blog = GhostWriter()