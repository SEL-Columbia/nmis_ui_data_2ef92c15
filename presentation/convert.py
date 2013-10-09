import json
import os

cwd = os.path.dirname(os.path.abspath(__file__))
fname = os.path.join(cwd, 'summary_sectors.json')


with open(fname, 'r') as f:
	data = json.loads(f.read())

data = data['relevant_data']['overview']

output = {
	'overview': data['overview_and_map']['ids'],
	'facility_overview': data['overview_facility_overview']['columns'],
	'mdg_status': data['overview_mdg_status']
}


out = json.dumps(output, indent=4)
path = os.path.join(cwd, 'lga_overview.json')
with open(path, 'w') as f:
	f.write(out)

