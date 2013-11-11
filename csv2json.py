import csv
import json
import os
import shutil


CWD = os.path.dirname(os.path.abspath(__file__))
OLD_DATA_DIR = os.path.join(CWD, 'old_data')
OUTPUT_DIR = os.path.join(CWD, 'data')

NORMALIZED_VALUES = {
    'NA': None,
    'NaN': None,
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
            value[header] = clean_csv_value(col)
        output.append(value)
    return output


def clean_csv_value(value):
    value = value.strip('"')
    try:
        value = int(value)
    except ValueError:
        try:
            if value not in ('Inf', '-Inf', 'NaN'):
                value = float(value)
        except ValueError:
            pass
    return NORMALIZED_VALUES.get(value, value)


def create_lga_files(data_folder):
    print 'Reading: ' + data_folder
    path = os.path.join(CWD, data_folder)
    lgas = {}
    facilities = []
    for fname in os.listdir(path):
        if not fname.endswith('.csv'):
            continue

        file_path = os.path.join(path, fname)
        with open(file_path, 'rb') as f:
            results = parse_csv(f)

        for item in results:
            if 'LGA' in fname and 'All' in fname:
                id = item['unique_lga']
                lgas[id] = item
            elif 'Facility' in fname:
                facilities.append(item)

    out_dir = os.path.join(OUTPUT_DIR, 'lgas')
    if os.path.exists(out_dir):
        print "output directory not empty, removing.."
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    for unique_lga, lga_data in lgas.iteritems():
        lga_data['unique_lga'] = unique_lga
        lga_data['facilities'] = [fac for fac in facilities if fac['unique_lga'] == unique_lga]
        try:
            out = json.dumps(lga_data, indent=4)
            path = os.path.join(out_dir, unique_lga + '.json')
            print 'Writing: ' + unique_lga + '.json'
            with open(path, 'w') as f:
                f.write(out)
        except Exception:
            print "#" * 50
            print "error in json dump: %s" % unique_lga


def create_zones():
    print 'Reading: districts.json'
    fname = os.path.join(OLD_DATA_DIR, 'geo', 'districts.json')
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

    print 'Writing zones.json'
    out = json.dumps(zones, indent=4)
    path = os.path.join(OUTPUT_DIR, 'zones.json')
    with open(path, 'w') as f:
        f.write(out)


def create_indicators():
    print 'Reading: variables.json'
    fname = os.path.join(OLD_DATA_DIR, 'variables', 'variables.json')
    with open(fname, 'r') as f:
        data = json.loads(f.read())

    indicators = {}
    for indicator in data['list']:
        indicators[indicator['slug']] = {
            'name': indicator['name'],
            'description': indicator['description']
        }

    print 'Reading: sectors.json'
    fname = os.path.join(OLD_DATA_DIR, 'variables', 'sectors.json')
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

    indicators['pop_2006'] = {
        'name': 'Population (2006)',
        'description': ''
    }

    print 'Writing: indicators.json'
    out = json.dumps(indicators, indent=4)
    path = os.path.join(OUTPUT_DIR, 'indicators.json')
    with open(path, 'w') as f:
        f.write(out)


def create_lga_view_files():
    fname = os.path.join(OLD_DATA_DIR, 'presentation', 'summary_sectors.json')
    with open(fname, 'r') as f:
        data = json.loads(f.read())

    overview_data = data['relevant_data']['overview']

    lga_overview = {
        'overview': overview_data['overview_and_map']['ids'],
        'facility_overview': overview_data['overview_facility_overview']['columns'],
        'mdg_status': overview_data['overview_mdg_status']
    }

    print 'Writing: lga_overview.json'
    out = json.dumps(lga_overview, indent=4)
    path = os.path.join(OUTPUT_DIR, 'lga_overview.json')
    with open(path, 'w') as f:
        f.write(out)

    print 'Writing: lga_sectors.json'
    sector_data = data['sectors']
    out = json.dumps(sector_data, indent=4)
    path = os.path.join(OUTPUT_DIR, 'lga_sectors.json')
    with open(path, 'w') as f:
        f.write(out)


def create_facility_tables():
    print 'Reading: sectors.json'
    fname = os.path.join(OLD_DATA_DIR, 'presentation', 'sectors.json')
    with open(fname, 'r') as f:
        data = json.loads(f.read())

    output = {}
    for sector_data in data['sectors']:
        tables = []
        output[sector_data['slug']] = tables
        
        indicators = sector_data['columns']
        indicators.sort(key=lambda x: x['display_order'])
        
        subgroups = sector_data['subgroups']
        subgroups.sort(key=lambda x: x['display_order'])
        for subgroup in subgroups:
            table = {'name': subgroup['name']}
            table['indicators'] = [i['slug'] for i in indicators \
                if subgroup['slug'] in i['subgroups']]
            tables.append(table)

    print 'Writing: facility_tables.json'
    out = json.dumps(output, indent=4)
    path = os.path.join(OUTPUT_DIR, 'facility_tables.json')
    with open(path, 'w') as f:
        f.write(out)


create_lga_files('data_774')
#create_zones()
#create_indicators()
#create_lga_view_files()
#create_facility_tables()






