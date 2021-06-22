#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A small example subscriber
"""
import paho.mqtt.client as paho
import time
import pandas as pd

def on_message(mosq, obj, msg):
    
    global dataset
    global start_time
    #终端检测数据
    print(msg.topic, msg.qos, msg.payload)
    #数据读取与存储
    insert_data = {}
    insert_data['sensor_number'] = msg.topic[6]
    if msg.topic[8] == 'h':
        insert_data['variable'] = 'humidity'
    elif msg.topic[8] == 't':
        insert_data['variable'] = 'temperature'
    else:
        insert_data['variable'] = 'error'
        print("Error: variable error.")
    insert_data['time'] = time.ctime()
    float_payload = float(msg.payload)
    insert_data['value'] = float_payload
    print(insert_data)
    dataset = dataset.append([insert_data])    
    #读取终止 ，将数据写入scv文件
    if (time.time() > start_time + interval):
        dataset.to_csv("C:\\Users\\Lenovo\\Desktop\\collected_data.csv")
    
def on_publish(mosq, obj, mid):
    pass

if __name__ == '__main__':
    start_time = time.time()
    interval = 0.2 * 60
    cols = ['sensor_number', 'variable', 'time', 'value']
    dataset = pd.DataFrame(columns=cols)
    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect("192.168.43.225", 1883, 600)
    client.subscribe("kids/yolo", 0)
    client.subscribe("adult/#", 0)
    client.subscribe("esp/#", 0)
    client.subscribe("weather/#", 0)
    client.subscribe("sensor1/#", 0)
    
    while client.loop() == 0:
        pass

# vi: set fileencoding=utf-8 :
