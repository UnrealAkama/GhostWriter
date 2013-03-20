from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates/'))


def gen_index():
	 
	template = env.get_template('index.html')

	output = template.render(foo='Hello World!')

	with open('output\index.html', 'w') as f:
		f.write(output)

def gen_content():

    template = env.get_template('content.html')

    output = template.render()

    with open('output\content.html', 'w') as f:
        f.write(output)

gen_index()
gen_content()