import json
import os

cwd = os.path.dirname(os.path.abspath(__file__))
fname = os.path.join(cwd, 'summary_sectors.json')


with open(fname, 'r') as f:
	data = json.loads(f.read())

overview_data = data['relevant_data']['overview']

lga_overview = {
	'overview': overview_data['overview_and_map']['ids'],
	'facility_overview': overview_data['overview_facility_overview']['columns'],
	'mdg_status': overview_data['overview_mdg_status']
}


out = json.dumps(lga_overview, indent=4)
path = os.path.join(cwd, 'lga_overview.json')
with open(path, 'w') as f:
	f.write(out)


sector_data = data['sectors']
out = json.dumps(sector_data, indent=4)
path = os.path.join(cwd, 'lga_sectors.json')
with open(path, 'w') as f:
	f.write(out)






