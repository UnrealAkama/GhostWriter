from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates/'))


def gen_index(self):
	 
	template = env.get_template('index.html')

	output_from_parsed_template = template.render(foo='Hello World!')

	with open('index.html', 'w') as f:
		f.write(output)

gen_index()
