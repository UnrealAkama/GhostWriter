from jinja2 import Environment, FileSystemLoader
from glob import glob
from markdown import markdown
from datetime import datetime
import shutil
import os


class GhostWriter(object):
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates/'))

        # Removes static content and re copies it
        shutil.rmtree(os.path.join('output', 'static'))
        shutil.copytree(os.path.join('content', 'static'), os.path.join('output', 'static'))

        # Create empty entries
        self.entries = list()

        # Run functions
        self.load_all()

        self.gen_content()

        self.gen_pages('index.html', 'index.html')

        self.gen_pages('feed.xml', 'feed.xml   ')

        print(self.entries)

    # Loads all entries from 'content/entries'
    def load_all(self):
        filenames = glob(os.path.join('content', 'entries', '*'))
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

            self.entries.append(dict(
                link=date + "-" + title.replace(' ', '-').lower() + '.html',
                title=title,
                date=date,
                tags=tags,
                raw=raw,
                html=markdown(raw)
            ))

        filenames = glob(os.path.join('content', 'projects', '*'))
        for file in filenames:
            raw = open(file, 'r').read()

        self.entries.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)

    # Output all entries to 'output/posts'
    def gen_content(self):
        template = self.env.get_template('content.html')

        for entry in self.entries:
            output = template.render(entry=entry)

            with open(os.path.join('output', entry['link']), 'w') as f:
                f.write(output)

    def gen_pages(self, templateName, outputName):
        template = self.env.get_template(templateName)

        output = template.render(entries=self.entries)

        with open(os.path.join('output', outputName), 'w') as f:
            f.write(output)


blog = GhostWriter()