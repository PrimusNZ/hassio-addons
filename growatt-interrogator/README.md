# Growatt Interrogator

## About

A simple (poorly written) python 3 script to interrogate a Growatt Inverter for power information and publishes to MQTT.
Optionally uploads data to [PVOutput.org](https://pvoutput.org) for tracking solar generation and overall consumption

Example: [Bus'Ted Solar Generation](https://pvoutput.org/list.jsp?userid=100056)

## DOES NOT WORK WITH HASSOS
HassOS lacks certain kernel modules required to correctly communicate with your inverter.
It is recommended to run this addon on top of [Home Assistant Supervised](https://github.com/home-assistant/supervised-installer)

## Requirements

- Growatt Invertor plugged into your Home Assistant instance via USB
- [Home Assistant Supervised](https://github.com/home-assistant/supervised-installer)
- (Optionally) PVOutput account with System ID and API Key