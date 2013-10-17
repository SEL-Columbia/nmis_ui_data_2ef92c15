import json
import os

cwd = os.path.dirname(os.path.abspath(__file__))
fname = os.path.join(cwd, 'sectors.json')


with open(fname, 'r') as f:
	data = json.loads(f.read())

output = {}

for sector in data['sectors']:
	slug = sector['slug']
	for column in sector['columns']:
		pass



out = json.dumps(output, indent=4)
path = os.path.join(cwd, 'facility_overview.json')
with open(path, 'w') as f:
	f.write(out)
