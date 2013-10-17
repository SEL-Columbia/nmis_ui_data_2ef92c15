import json
import os


"""
Convert to this:
output = {
	"Zone Name": { 
		"State Name": {
			"LGA Name", "unique_lga"
		}
	}
}
"""

cwd = os.path.dirname(os.path.abspath(__file__))
fname = os.path.join(cwd, 'districts.json')


with open(fname, 'r') as f:
	data = json.loads(f.read())

zones = {}
zone_data = [g for g in data['groups'] if 'group' not in g]
state_data = [g for g in data['groups'] if 'group' in g]


for zone in zone_data:
	zone_name = zone['label']
	zone_id = zone['id']

	states = {}
	zones[zone_name] = states
	for state in state_data:
		if state['group'] != zone_id:
			continue
		lgas = {}
		state_name = state['label']
		state_id = state['id']
		states[state_name] = lgas

		for lga in data['districts']:
			if lga['group'] == state_id:
				lga_name = lga['name']
				unique_lga = lga['data_root'].split('/')[1]
				lgas[lga_name] = unique_lga


out = json.dumps(zones, indent=4)
path = os.path.join(cwd, 'zones.json')
with open(path, 'w') as f:
	f.write(out)



