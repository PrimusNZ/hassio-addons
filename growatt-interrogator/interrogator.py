#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for fetching data from Growatt inverter for MQTT
"""
import subprocess
from time import strftime
import time
from configobj import ConfigObj
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import os
from paho.mqtt import client as mqtt_client
import random
import threading
import signal
import requests

# read settings from config file
config = ConfigObj("/tmp/pvinverter.cfg")
InverterPort = config['Inverter']
MqttBroker = config['MQTTBroker']
MqttPort = int(config['MQTTPort'])
MqttUser = config['MQTTUser']
MqttPass = config['MQTTPass']

# PVOutput Configurations
PVOEnabled = config['PVOEnabled']
SystemID = config['SystemID']
APIKey = config['APIKey']

Verbose = config['Verbose']


# Static settings
MqttStub = "Growatt"
MqttTopicPower = "power_mode"
MqttTopicCharge = "charge_mode"
ReadRegisters = 101
client_id = f'inverter-stats-{random.randint(0, 1000)}'


Inverter = ModbusClient(method='rtu', port=InverterPort, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
Inverter.connect()

def send_state(client, time_now):
  data = dict()

  try:
    # Sending Current State
    holding_registers = Inverter.read_holding_registers(0,3)
    input_registers = Inverter.read_input_registers(0,ReadRegisters)

    state = holding_registers.registers[1]
    if state == 0:
      data['state_power'] = "Battery First"
    elif state == 1:
      data['state_power'] = "Solar First"
    elif state == 2:
      data['state_power'] = "Grid First"
    elif state == 3:
      data['state_power'] = "Solar and Grid First"

#    holding_registers = Inverter.read_holding_registers(2,1)
    state = holding_registers.registers[2]
    if state == 0:
      data['state_charge'] = "Solar First"
    elif state == 1:
      data['state_charge'] = "Solar and Grid"
    elif state == 2:
      data['state_charge'] = "Solar Only"

    value=int(input_registers.registers[0])
    status="Standby"
    if value==0:
        status="Standby"
    elif value==1:
        status="Unknown"
    elif value==2:
        status="Discharge"
    elif value==3:
        status="Fault"
    elif value==4:
        status="Flash"
    elif value==5:
        status="PV Charge"
    elif value==6:
        status="AC Charge"
    elif value==7:
        status="Combine Charge"
    elif value==8:
        status="Combine Charge and Bypass"
    elif value==9:
        status="PV Charge and Bypass"
    elif value==10:
        status="AC Charge and Bypass"
    elif value==11:
        status="Bypass"
    elif value==12:
        status="PV Charge and Discharge"
    else:
        status="ERROR"

    data['inverter_status']=status

    value=input_registers.registers[1]
    data["pv_volts"]=float(value)/10

    value=input_registers.registers[4]
    data["pv_power"]=int(value)/10

    value=input_registers.registers[10]
    data["consumption"]=int(value)/10

    value=input_registers.registers[12]
    data["inverter_voltamps"]=float(value)/1000

    value=int(input_registers.registers[14])+int(input_registers.registers[70])
    data["ac_power"]=int(value)/10

    value=input_registers.registers[17]
    data['batt_volts']=float(value)/100

    value=input_registers.registers[18]
    data['batt_soc']=int(value)

    value=input_registers.registers[20]
    data["grid_volts"]=float(value)/10

    value=input_registers.registers[21]
    data["grid_frequency"]=float(value)/100

    value=input_registers.registers[22]
    data["inverter_volts"]=float(value)/10

    value=input_registers.registers[23]
    data["inverter_frequency"]=float(value)/100

    value=input_registers.registers[27]
    data["inverter_load"]=float(value)/10

    value=input_registers.registers[51]
    data["solar_hist_total"]=value*100

    value=input_registers.registers[63]
    data["batt_hist_total"]=value*100

    value=input_registers.registers[67]+input_registers.registers[59]
    data["ac_hist_total"]=value*100

    value=input_registers.registers[51]+input_registers.registers[59]
    data["charge_hist_total"]=value*100

    value=input_registers.registers[74]
    data["batt_consumption"]=round(float(value)/10,0)

    value=input_registers.registers[61]
    data["batt_consumption_today"]=round(float(value)/10,0)

    value=input_registers.registers[83]
    data["charge_current"]=round(float(value)/10,0)

    value=input_registers.registers[19]
    data["charge_volts"]=float(value)/100

    data["charge_power"]=round(data["charge_current"] * data["charge_volts"],0)

    data["batt_power"]=data["batt_consumption"] - data["charge_power"]

    data["inverter_fan_speed"]=input_registers.registers[82]

    data["inverter_temp"]=input_registers.registers[25]/10
    data["dcdc_temp"]=input_registers.registers[26]/10

    data["consumption_total"] = data["ac_hist_total"]+data["batt_hist_total"]
    data["consumption_combined"] = data["consumption"]+data["charge_power"]

    for key, value in sorted(data.items()):
        publish(client, key, value)

    if PVOEnabled.lower() == 'true':
        if time.time() >= (time_now+300):
            time_now = time.time()
            pv_upload(data)
  except:
    print("Exception while sending state")

  threading.Timer(1,send_state,args=[client,time_now]).start()

def pv_upload(data):
    t_date = format(strftime('%Y%m%d'))
    t_time = format(strftime('%H:%M'))
    url="http://pvoutput.org/service/r2/addstatus.jsp"
    upload={'d':t_date,'t':t_time,'v2':data["pv_power"],'v4':data["consumption"],'v6':data["pv_volts"],'c1':"0"}
    api_headers={'X-Pvoutput-Apikey':APIKey,'X-Pvoutput-SystemId':SystemID}

    x = requests.post(url, data = upload, headers = api_headers)
    if Verbose.lower() == 'true':
        print("%s %s: Pushed data to PVOutput.org - %s" %(t_date, t_time, x.text))

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            topic1 = ('%s/%s' %(MqttStub, MqttTopicPower))
            client.subscribe(topic1, qos=0)
            topic2 = ('%s/%s' %(MqttStub, MqttTopicCharge))
            client.subscribe(topic2, qos=0)

            send_state(client, 0)
        else:
            print("Failed to connect, return code %d\n", rc)
            quit()

    #def on_subscribe(client, userdata, mid, granted_qos):
    #    print(mid)
    #    topic = ('%s/%s' %(MqttStub, MqttTopicPower))
    #    print("Subscribed to '%s'" %(topic))

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(MqttUser, MqttPass)
    client.on_connect = on_connect
    #client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(MqttBroker, MqttPort)
    return client


def on_message(client,userdata,message):
    topic = message.topic
    msg = message.payload.decode("utf-8")
    if Verbose.lower() == 'true':
        print("Received message: '%s' on '%s'" %(msg,topic))

    valid=False
    try:

        if topic == ('%s/%s' %(MqttStub, MqttTopicPower)):
            if msg == "Battery First":
                set_register(1,0)
                publish(client, "state_power", msg)
            elif msg == "Solar First":
                set_register(1,1)
                publish(client, "state_power", msg)
            elif msg == "Grid First":
                set_register(1,2)
                publish(client, "state_power", msg)
            elif msg == "Solar and Grid First":
                set_register(1,3)
                publish(client, "state_power", msg)
        if topic == ('%s/%s' %(MqttStub, MqttTopicCharge)):
            if msg == "Solar First":
                set_register(2,0)
                publish(client, "state_charge", msg)
            elif msg == "Solar and Grid":
                set_register(2,1)
                publish(client, "state_charge", msg)
            elif msg == "Solar Only":
                set_register(2,2)
                publish(client, "state_charge", msg)
    except:
      print("Exception while changing state")

def publish(client,stub,data):
    topic = ('%s/%s' %(MqttStub, stub))
    client.publish(topic, data)
    if Verbose.lower() == 'true':
        print("Published '%s' to '%s'" %(data, topic))

def run():
    print("Growatt Interrogator Initialising")
    print("Verbose: %s", %(Verbose.lower()))
    client = connect_mqtt()
    print("Up and Running!")
    client.loop_forever()

def set_register(register,value):
    success = False

    while success != True:
        try:
            # Read data from inverter
            holding_registers = Inverter.read_holding_registers(register,1)
            print ('%s -> %s' %(holding_registers.registers[0], value))
            Inverter.write_registers(register,value)

        except:
            print("Exception sending state change")
            time.sleep(1)
        else:
            success = True

if __name__ == '__main__':
    run()
