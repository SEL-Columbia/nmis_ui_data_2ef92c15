import json
import os

cwd = os.path.dirname(os.path.abspath(__file__))
fname = os.path.join(cwd, 'variables.json')


with open(fname, 'r') as f:
	data = json.loads(f.read())

output = {}
for indicator in data['list']:
	output[indicator['slug']] = {
		'name': indicator['name'],
		'description': indicator['description']
	}


out = json.dumps(output, indent=4)
path = os.path.join(cwd, 'indicators.json')
with open(path, 'w') as f:
	f.write(out)

