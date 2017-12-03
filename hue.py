import json
import sys

import argparse

import requests

API_BASE_URL = "http://{bridge}/api/{user}"

class Light(object):
    def __init__(self, base_url, _id, resp):
        self.state = resp["state"]
        self.name = resp["name"]
        self.uniqueid = resp["uniqueid"]
        self.id = _id
        self.base_url = base_url + "/lights/{id}".format(id=self.id)
        self.data = resp

    @property
    def on(self):
        return self.state['on']

    def turn_on(self):
        payload = {"on": True}
        url = self.base_url + "/state"
        return requests.put(url, data=json.dumps(payload))

    def turn_off(self):
        payload = {"on": False}
        url = self.base_url + "/state"
        return requests.put(url, data=json.dumps(payload))

class Bridge(object):
    def __init__(self, addr, username):
        self.__addr = addr
        self.__username = username
        self.base_url = API_BASE_URL.format(bridge=addr, user=username)

    def lights(self):
        url = self.base_url + "/lights"
        r = requests.get(url)
        lights = []
        for k, v in r.json().iteritems():
            lights.append(Light(self.base_url, k, v))
        return lights

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("id", nargs="?", type=int, default=None)
    parser.add_argument("command", nargs="?", default="status")
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()

    # TODO: Handle IOError and ValueError (json)
    with open("creds.json") as f:
        creds = json.load(f)

    b = Bridge(creds['bridge'], creds['username'])
    lights = b.lights()

    if args.id:
        light_id = args.id - 1
        if args.command == "on":
            print('turning on light {id}'.format(id=args.id))
            lights[light_id].turn_on()
        elif args.command == "off":
            print('turning off light {id}'.format(id=args.id))
            lights[light_id].turn_off()
        elif args.command == "status":
            if lights[light_id].on:
                status = 'on'
            else:
                status = 'off'
            print(status)
    else:
        for light in lights:
            print(light.data)
