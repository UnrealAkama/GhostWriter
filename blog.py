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

        # Creates the output folder
        if not os.path.exists('output'):
            os.makedirs('output')

        # Removes static content and re copies it
        shutil.rmtree(os.path.join('output'))
        shutil.copytree(os.path.join('content', 'static'),
                        os.path.join('output', 'static'))

        # Create empty entries
        self.entries = list()
        self.projects = list()
        self.aboutme = list()

        # Run functions
        self.load(self.entries, 'entries')
        self.load(self.projects, 'projects')
        self.load(self.aboutme, 'aboutme')

        self.gen_page('content.html', '', self.entries)
        self.gen_pages('index.html', 'index.html', self.entries)
        self.gen_pages('feed.xml', 'feed.xml', self.entries)
        self.gen_pages('projects.html', 'projects.html', self.projects)
        self.gen_pages('aboutme.html', 'aboutme.html', self.aboutme)

    '''
        Loads all entries from a folder, and stores them in the argument 'stored'.
        Uses markdown to translate the plain text to html, the metadate is taken from the first lines.
        Explain metadata is
            #title This is an example title
            #date 2013-04-08
            #tags demo sample
    '''
    def load(self, stored, location):
        filenames = glob(os.path.join('content', location, '*'))
        for file in filenames:
            raw = open(file, 'r').read()
            title = None
            date = None
            image = None
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
                if item == 'image':
                    image = rest
                if item == 'tags':
                    tags = rest.split(' ')

            stored.append(dict(
                link=date + "-" + title.replace(' ', '-').lower() + '.html',
                title=title,
                date=datetime.strptime(date, '%Y-%m-%d'),
                tags=tags,
                raw=raw,
                image=image,
                html=markdown(raw)
            ))

        # stored.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        stored.sort(key=lambda x: x['date'], reverse=True)

        # for entry in stored:
            # formated_data = datetime.strptime(entry['date'], '%Y-%m-%d')
            # entry['date'] = formated_data.strftime("%B %d, %Y")

    '''
        Generates a single page or number of single pages. The data for the pages is based in via the content paramater.
        If you want to generate just one page, pass the content argument as a list with only one element inside of it.
    '''
    def gen_page(self, templateName, outputName, content):
        template = self.env.get_template(templateName)

        for entry in content:
            output = template.render(entry=entry)

            with open(os.path.join('output', outputName, entry['link']), 'w') as f:
                f.write(output)

    '''
        Generates a single page that may have a number of elements or contents in it. Be sure that items is a list.
    '''
    def gen_pages(self, templateName, outputName, items):
        template = self.env.get_template(templateName)

        output = template.render(content=items)

        with open(os.path.join('output', outputName), 'w') as f:
            f.write(output)

if __name__=='__main__':
    GhostWriter()
