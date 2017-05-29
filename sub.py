#!/usr/bin/env python
import paho.mqtt.client as mqtt
graphite_host='heidi.shack'
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("/#")
    #client.subscribe("/temperature/#")
    #client.subscribe("/humidity/#")


import socket
def to_graphite(path,data,ts=None,host='localhost',port=2003):
    if not ts: ts = datetime.now().timestamp()
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

def on_message(client, userdata, msg):
    t = msg.topic
    print(t)
    if t.startswith('/temperature') or t.startswith('/humidity'):
        typ=t.split('/')[1]
        ident=t.split('/')[-1]
        to_graphite("sensors.temp.id.{}.{}".format(ident,typ),float(msg.payload),int(msg.timestamp),host=graphite_host)
    if t.startswith('/timer'):
        typ=t.split('/')[2]
        ident=t.split('/')[-1]
        to_graphite("sensors.timer.{}.{}".format(ident,typ),float(msg.payload),int(msg.timestamp),host=graphite_host)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("heidi.shack", 1883, 60)
client.connect("hass.shack", 1883, 60)

client.loop_forever()
