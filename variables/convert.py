import json
import os

cwd = os.path.dirname(os.path.abspath(__file__))
fname = os.path.join(cwd, 'variables.json')
with open(fname, 'r') as f:
	data = json.loads(f.read())

indicators = {}
for indicator in data['list']:
	indicators[indicator['slug']] = {
		'name': indicator['name'],
		'description': indicator['description']
	}


fname = os.path.join(cwd, 'sectors.json')
with open(fname, 'r') as f:
	data = json.loads(f.read())

for sector in data['sectors']:
	for column in sector['columns']:
		slug = column['slug']
		if slug not in indicators:
			indicators[slug] = {
				'name': column['name'],
				'description': column.get('description', '')
			}


out = json.dumps(indicators, indent=4)
path = os.path.join(cwd, 'indicators.json')
with open(path, 'w') as f:
	f.write(out)

