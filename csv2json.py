import csv
import json
import os
import shutil
import zipfile



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

def zip_download(in_folder, out_dir):
    out_name = 'nmis_data'
    out_file = os.path.join(out_dir, out_name)
    if os.path.exists(out_file):
        print "found existing %s, removing" % out_file
        os.remove(out_file)
    shutil.make_archive(out_file, 'zip', in_folder)
    print "created zip file %s" % out_name

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
        out = json.dumps(lga_data, indent=4, ensure_ascii=True)
        path = os.path.join(out_dir, unique_lga + '.json')
        print 'Writing: ' + unique_lga + '.json'
        with open(path, 'w') as f:
            f.write(out)

    zip_download(data_folder, OUTPUT_DIR)

    
    

create_lga_files('data_774')



