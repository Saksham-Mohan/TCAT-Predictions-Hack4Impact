import requests
import json
import threading
from time import time
import os

PATH = './data/'

def request_data():
    '''
    Requests data from TCAT live data feed. Returns the JSON without the (unneeded) metadata. 
    '''
    r = requests.get('https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate&debug=true')
    if not r:
        print('Error getting data from URL! {} Error.'.format(r.status_code))
    json_dict = json.loads(r.text)
    return json_dict['Entities']

def extract_data(entity):
    '''
    Extract specific data from the JSON, 
    '''
    j = {}
    j['TripId'] = entity['Id']
    if entity['TripUpdate']:
        trip_update = entity['TripUpdate']
        j['RouteId'] = trip_update['Trip']['RouteId']
        j['StartDate'] = trip_update['Trip']['StartDate']
        vehicle = trip_update.get('Vehicle', None)
        if vehicle:
            j['VehicleId'] = vehicle['Id']
    if entity['TripUpdate']['StopTimeUpdates']:
        j['stop_time_updates'] = entity['TripUpdate']['StopTimeUpdates']
    return j

def save_data(current_time):
    '''
    Parses all entity/bus data for a time t, saves it locally.
    
    directory path: path to which 
    current_time: unix time recorded, representing timestep t
    '''
    entity_list = request_data()
    for entity in entity_list:
        entity_data = extract_data(entity)
        entity_data['time_recorded'] = current_time
        col_name = str(entity['Id'])
        path_name = '{}{}.json'.format(PATH, col_name)
        mode = 'a' if os.path.exists(path_name) else 'w'
        with open(path_name, mode) as outfile:
            if mode == 'a':
                outfile.write('\n')
            json.dump(entity_data, outfile)

def parse_by_seconds():
    '''
    checks live feed every 30 seconds
    '''
    threading.Timer(30.0, parse_by_seconds).start()
    print('<<< running trip-update...')
    save_data(int(time()))
    print("...ran trip-update >>>")

if __name__ == "__main__":
    with open("password.txt", "r") as f:
        username = f.readline().strip()
        password = f.readline().strip()
        url = 'mongodb+srv://{}:{}@cluster0-ydcpr.mongodb.net/test?retryWrites=true&w=majority'.format(username, password)
    myclient = pymongo.MongoClient(url)
    db = myclient["trip-updates"]
    print('starting program...\n')
    parse_by_seconds()