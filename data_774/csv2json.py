import csv
import json
import os



NORMALIZED_VALUES = {
	'NA': None,
	'TRUE': True,
	'yes': True,
	'Yes': True,
	'FALSE': False,
	'no': False,
	'No': False
}


def parse_csv(file):
	print 'Parsing: ' + file.name
	output = []
	reader = csv.reader(file, delimiter=',', quotechar='"')
	headers = [h.strip('"') for h in reader.next()]
	for row in reader:
		value = {}
		for header, col in zip(headers, row):
			value[header] = clean_value(col)
		output.append(value)
	return output


def clean_value(value):
	value = value.strip('"')
	value = NORMALIZED_VALUES.get(value, value)
	try:
		value = int(value)
	except:
		try:
			value = float(value)
		except:
			pass
	return value



def convert_files():
	cwd = os.path.dirname(os.path.abspath(__file__))
	lgas = {}
	facilities = []
	for fname in os.listdir(cwd):
		if not fname.endswith('.csv'):
			continue

		with open(fname, 'rb') as f:
			results = parse_csv(f)

		for item in results:
			if 'LGA' in fname and 'All' in fname:
				id = item.pop('unique_lga')
				lgas[id] = item
			elif 'Facility' in fname:
				facilities.append(item)

	out_dir = os.path.join(cwd, 'lgas')
	os.makedirs(out_dir)

	for unique_lga, lga_data in lgas.iteritems():
		lga_data['unique_lga'] = unique_lga
		lga_data['facilities'] = [fac for fac in facilities if fac['unique_lga'] == unique_lga]
		out = json.dumps(lga_data, indent=4)

		path = os.path.join(out_dir, unique_lga + '.json')
		print 'Writing: ' + unique_lga + '.json'
		with open(path, 'w') as f:
			f.write(out)

convert_files()



