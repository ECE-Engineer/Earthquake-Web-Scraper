import string
import os
import sys
import datetime
import json
import requests as rqst
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def collect_data(url):
  try:
    with closing(get(url, stream=True)) as resp:
      if is_valid_resp(resp):
        print('valid url')
        return resp.content
      else:
        print('invalid url')
        return None
  except RequestException as e:
    display_errors('Error during requests to {0} : {1}'.format(url, str(e)))
    return None

def is_valid_resp(resp):
  content_type = resp.headers['Content-Type'].lower()
  return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def display_errors(e):
  print(e)

def main():
  us_min_lat = 'minlatitude=' + '24.6'
  us_max_lat = 'maxlatitude=' + '50'
  us_min_lon = 'minlongitude=' + '-125'
  us_max_lon = 'maxlongitude=' + '-65'
  min_mag = 'minmagnitude=' + '6.3'
  stringQuery = ['format=geojson','starttime=1500-01-01','endtime=2018-11-11', 'eventtype=earthquake', (us_min_lat), (us_max_lat), (us_min_lon), (us_max_lon), (min_mag), 'orderby=time-asc']
  website_string = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&'
  input_string = website_string + '&'.join(stringQuery)
  data = (get(input_string)).json()
  data_amount = len(data['features'])
  
  f = open('earthquakes.txt', 'w')
  for i in range(0, data_amount):
    loc = data['features'][i]['properties']['place']
    time = data['features'][i]['properties']['time']
    depth = data['features'][i]['geometry']['coordinates'][2]
    mag = data['features'][i]['properties']['mag']
    time = datetime.datetime.utcfromtimestamp(time/1000)
    print(time)
    
    f.write('location:\t' + loc)
    f.write('time:\t' + str(time))
    f.write('\tdepth:\t' + str(depth) + ' km')
    f.write('\tmag:\t' + str(mag) + '\n')
  f.close()

if __name__ == '__main__':
  main()
