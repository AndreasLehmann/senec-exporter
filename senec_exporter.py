import os
import re

import json
from time import sleep
from urllib.request import urlopen

import senec_util

# install -> pip install prometheus-client

from prometheus_client import Gauge, Info, start_http_server, Counter

## IP adress from SENEC PV 
senec_ip_adress = '192.168.9.91'
sample_rate = 10 # fetch data every 10 seconds

# Prometheus Gauges
prom_Info = Info('energy_senec_info','Informationen zur SENEC PV Anlage')
prom_EVU_Bezug_Watt = Gauge("energy_EVU_Bezug_Aktuell_W","Aktueller Energiebezug/-Einspeisung aus/in das Netz des EVU in Watt")
prom_Hausverbrauch_Watt = Gauge("energy_Hausverbrauch_Aktuell_W","Aktueller Gesamtverbrauch des Hauses in Watt")
prom_PV_Erzeugung_Watt = Gauge("energy_PV_Erzeugung_Aktuell_W","Aktuell erzeugte Leistung der PV-Anlage in Watt")
prom_Batterie_Entladung_Watt = Gauge("energy_Batterie_Entladung_Aktuell_W","Aktuelle Batterie Ladung/Entladung in Watt")
prom_Batterie_SOC_Prozent = Gauge("energy_Batterie_SOC_Prozent","Aktueller Ladezustand der Batterie in Prozent")
prom_feed_limit_percent = Gauge("energy_Einspeisebegrenzung_Prozent","Aktuelle Einspeisebegrenzung in Prozent")
prom_batt_Volt = Gauge("energy_Battery_Voltage_V","Batteriespannung in Volt",labelnames=['battery'],unit='V')
prom_batt_Ampere = Gauge("energy_Battery_Current_A","Batteriestrom in Ampere",labelnames=['battery'],unit='A')
prom_batt_Watt = Gauge("energy_Battery_Power_W","Batterieleistung in Watt",labelnames=['battery'],unit='W')

prom_supplier_Voltage_V = Gauge("energy_EVU_Spannung_V","Netzspannung in Volt",labelnames=['phase'],unit='V')
prom_suppler_Current_A = Gauge("energy_EVU_Strom_A","Netzstrom in Ampere",labelnames=['phase'],unit='A')
prom_suppler_Power_W = Gauge("energy_EVU_Leistung_W","Netzleistung in Watt",labelnames=['phase'],unit='W')

def main():
    start_http_server(8000)

    # infinite loop
    while True:
        update_metrics()
        sleep (sample_rate)

def read_senec_data(json_query):
    response = urlopen('http://' + senec_ip_adress + '/lala.cgi',data=json_query.encode('utf-8'))
    return json.load(response)


def update_metrics():
    print("collecting metrics from " + senec_ip_adress)

    #########################################
    ## read Energy supplier data
    query = '{"PM1OBJ1":{"FREQ":"","U_AC":"","I_AC":"","P_AC":"","P_TOTAL":""}}'
    jsondata = read_senec_data(query)
    #print(jsondata)

    # Energy consumption from supplier (supplier total) (W) Werte -3000  >> 3000
    prom_EVU_Bezug_Watt.set( round(
                senec_util.decode(jsondata['PM1OBJ1']['P_TOTAL']),0))

    # supplier provided voltage
    prom_supplier_Voltage_V.labels(phase=1).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['U_AC'][0]),1))
    prom_supplier_Voltage_V.labels(phase=2).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['U_AC'][1]),1))
    prom_supplier_Voltage_V.labels(phase=3).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['U_AC'][2]),1))

    # supplier provided current
    prom_suppler_Current_A.labels(phase=1).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['I_AC'][0]),1))
    prom_suppler_Current_A.labels(phase=2).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['I_AC'][1]),1))
    prom_suppler_Current_A.labels(phase=3).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['I_AC'][2]),1))

    # supplier provided power
    prom_suppler_Power_W.labels(phase=1).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['P_AC'][0]),1))
    prom_suppler_Power_W.labels(phase=2).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['P_AC'][1]),1))
    prom_suppler_Power_W.labels(phase=3).set( round(
                senec_util.decode(jsondata['PM1OBJ1']['P_AC'][2]),1))            

    #########################################
    ## read battery data
    query = '{"ENERGY":{"GUI_BAT_DATA_FUEL_CHARGE":"","GUI_BAT_DATA_POWER":"","GUI_BAT_DATA_VOLTAGE":"","GUI_BAT_DATA_OA_CHARGING":"","GUI_HOUSE_POW":"","GUI_INVERTER_POWER":""}}'
    jsondata = read_senec_data(query)
    #print(jsondata)
    
    # GUI: House consumption 
    prom_Hausverbrauch_Watt.set( round(
                senec_util.decode(jsondata['ENERGY']['GUI_HOUSE_POW']),0))

    # GUI: Generated solar power
    prom_PV_Erzeugung_Watt.set( round(
                senec_util.decode(jsondata['ENERGY']['GUI_INVERTER_POWER']),0))

    # battery power (W)  -345 (discharge) >> 1200 (charge)
    prom_Batterie_Entladung_Watt.set( round(
                senec_util.decode(jsondata['ENERGY']['GUI_BAT_DATA_POWER']),0))

    # Battery state of charge (SOC)  10 >> 55 >> 100
    prom_Batterie_SOC_Prozent.set( round(
                senec_util.decode(jsondata['ENERGY']['GUI_BAT_DATA_FUEL_CHARGE']),0))



    #########################################
    ## read statistic data from SENEC PV
    query = '{"STATISTIC":{"CURRENT_STATE":"","LIVE_BAT_CHARGE":"","LIVE_BAT_DISCHARGE":"","LIVE_GRID_EXPORT":"","LIVE_GRID_IMPORT":"","LIVE_HOUSE_CONS":"","LIVE_PV_GEN":""}}'
    jsondata = read_senec_data(query)
    #print(jsondata)

    # current status meaassge
    
    status_code = senec_util.decode(jsondata['STATISTIC']['CURRENT_STATE'])
    status_message = senec_util.SYSTEM_STATE_NAME[ status_code ]
    prom_Info.info({'status': status_message , 'ip':'?'})
    
    #########################################
    ## read pv (battery) data
    query = '{"PV1":{"POWER_RATIO":"","MPP_VOL":"","MPP_CUR":"","MPP_POWER":""}}'
    jsondata = read_senec_data(query)
    #print(jsondata)

    # power feeding limit
    prom_feed_limit_percent.set( round(
                senec_util.decode(jsondata['PV1']['POWER_RATIO']),1))

    # battery voltage
    prom_batt_Volt.labels(battery=0).set( round(
                senec_util.decode(jsondata['PV1']['MPP_VOL'][0]),1))
    prom_batt_Volt.labels(battery=1).set( round(
                senec_util.decode(jsondata['PV1']['MPP_VOL'][1]),1))
    prom_batt_Volt.labels(battery=2).set( round(
                senec_util.decode(jsondata['PV1']['MPP_VOL'][2]),1))

    # battery current
    prom_batt_Ampere.labels(battery=0).set( round(
                senec_util.decode(jsondata['PV1']['MPP_CUR'][0]),1))
    prom_batt_Ampere.labels(battery=1).set( round(
                senec_util.decode(jsondata['PV1']['MPP_CUR'][1]),1))
    prom_batt_Ampere.labels(battery=2).set( round(
                senec_util.decode(jsondata['PV1']['MPP_CUR'][2]),1))

    # battery power
    prom_batt_Watt.labels(battery=0).set( round(
                senec_util.decode(jsondata['PV1']['MPP_POWER'][0]),1))
    prom_batt_Watt.labels(battery=1).set( round(
                senec_util.decode(jsondata['PV1']['MPP_POWER'][1]),1))
    prom_batt_Watt.labels(battery=2).set( round(
                senec_util.decode(jsondata['PV1']['MPP_POWER'][2]),1))

if __name__ == '__main__':
    main()
