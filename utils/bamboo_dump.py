import os
from pybamboo.connection import Connection
from pybamboo.dataset import Dataset
import re
import simplejson as json
import sys
import time


def load_json(json_path):
  with open(json_path) as f:
    return json.loads(f.read())

def write_json(json_path, content):
  #with open(json_path, mode='w', encoding='utf-8') as f:

  with open(json_path, mode='w') as f:
    f.write(content)

def convert_data(data_path):
    reg_string = r'districts/([a-z_]+)/data/(education|health|water|lga_data).(csv|json)'
    reg_match = re.match(reg_string, data_path)
    if reg_match:
        state_lga, sector, ext = reg_match.groups()
        print "lga: %s, sector: %s, ext: %s" % (state_lga, sector, ext)
        if sector == 'water':
            bamboo_id = bamboo_hash['Water_Facilities']['bamboo_id']
        if sector == 'education':
            bamboo_id = bamboo_hash['Education_Facilities']['bamboo_id']
        if sector == 'health':
            bamboo_id = bamboo_hash['Health_Facilities']['bamboo_id']
        if sector == 'lga_data':
            bamboo_id = bamboo_hash['LGA_Data']['bamboo_id']
        begin = time.time()
        bamboo_ds = Dataset(dataset_id=bamboo_id)
        ffdata = bamboo_ds.get_data(query={'unique_lga': state_lga}, format=ext)
        #retry
        if len(ffdata) is 0:
          print "XXXbamboo fails, retry"
          ffdata = bamboo_ds.get_data(query={'unique_lga': state_lga}, format=ext)

        if sector == 'lga_data':
            ffdata = ffdata[0]
            ffdata = {'data': [{'id': str(key), 'value': str(value)}\
                for key, value in ffdata.iteritems()]}

            ffdata = json.dumps(ffdata)
        print "saving data to %s" % data_path
        write_json(data_path, ffdata)
        end = time.time()
        time_delta = end - begin
        print 'finished %s %s, used %s' %(state_lga, sector, time_delta)


def get_lga_data(lga):
  lga_path = 'districts/%s/data' % lga
  convert_data('%s/education.csv' % lga_path)
  convert_data('%s/health.csv' % lga_path)
  convert_data('%s/water.csv' % lga_path)
  convert_data('%s/lga_data.json' % lga_path)


if __name__ == '__main__':
  bamboo_hash = load_json('utils/bamboo_hash.json')
  unique_lgas = load_json('utils/unique_lga.json')
  if len(sys.argv) > 1:
    last_one = sys.argv[1]
    unique_lgas = unique_lgas[unique_lgas.index(last_one)+1:]

  for lga in unique_lgas:
    get_lga_data(lga)

