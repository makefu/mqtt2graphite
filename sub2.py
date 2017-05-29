#!/usr/bin/env python
import paho.mqtt.client as mqtt
from datetime import datetime
graphite_host='heidi.shack'
db = {}
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("/#")
    #client.subscribe("/temperature/#")
    #client.subscribe("/humidity/#")


import socket
def to_graphite(path,data,ts=None,host='localhost',port=2003):
    if not ts: ts = int(datetime.now().timestamp())
    sock = socket.socket()
    data="{} {} {}\n".format(path,data,ts)
    try:
        sock.connect((host, port))
        sock.sendall(data.encode())
        sock.close()
        print("sent '{}'".format(data.strip()))
    except Exception as e:
        print(e)
        print("cannot send message '{}'".format(data))


def lookup_name(ident):
    return db[ident]

def on_message(client, userdata, msg):
    t = msg.topic
    p = msg.payload
    # print(t)
    if t.endswith('/temperature') or t.endswith('/humidity'):
        typ=t.split('/')[-1]
        ident=t.split('/')[-2]
        try:
            to_graphite("homeassistant.{}.{}".format(lookup_name(ident),typ),float(msg.payload),host=graphite_host)
        except LookupError:
            print("cannot look up {}".format(ident))
    elif t.endswith('/name'):
        ident=t.split('/')[-2]
        db[ident] = msg.payload.decode()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("heidi.shack", 1883, 60)
client.connect("hass.shack", 1883, 60)

client.loop_forever()
