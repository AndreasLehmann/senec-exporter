# Prometheus Exporter für SENEC PV Anlage

Der senec_exporter stellt die Anlagendaten des PV-Wechselrichters im Prometheus Format zur Verfügung.

Thanks to Nancy Chauhan for sharing her HTTP Exporter sample: 
https://levelup.gitconnected.com/building-a-prometheus-exporter-8a4bbc3825f5

Getestet mit **SENEC.Home V3 hybrid duo** mit 3 x 2,5 kWh Akkus. Andere SENEC Wechselrichter sollten ebenfalls funktionieren. Basis für den Exporter ist das lala.cgi Skript auf der Web-Seite des Wechselrichters.

Funktionsweise: Die Anlagendaten werden per HTTP aus dem Wechselrichter gelesen und über einen eigene HTTP-Server im Prometheus-Format bereitgestellt. Außerdem ist noch eine Aufbereitung im json-Format vorgesehen, um Pull-Basierte Abfragen der Anlagendaten zu ermöglichen. Zum Beispiel mit node-red.

Mögliche Parameter für das Exporter Skript:

```
-ip / --senec-ip = ip address of the senec device e.g. 192.168.1.7 (required) 

-r / --rate = sampling rate in seconds (default=20)

-p / --port = HTTP-Server port where the Prometheus data will be exposed (default=8000)
```

Start locally with:

```
python3 senec_exporter.py -ip 192.168.1.7 -r 5
```

Create a Docker Image with:

`docker build -t senec_exporter_app -f docker/Dockerfile .`

Start with:

`docker run -p 8000:8000 --restart unless-stopped --name senec_exporter senec_exporter_app`

->> http://localhost:8000/

->> http://localhost:8000/metrics

->> http://localhost:8000/json
