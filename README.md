# Prometheus Exporter für SENEC PV Anlage



> **ACHTUNG:** Seit 9/2023 gibt es ein Firmware-Update, bei dem SENEC von http auf https umgestellt hat (und dabei mit einem ungüligen SSL Zertifiak arbeitet :-( ). Diese Umstellung ist hier bereits berücksichtigt. Allerdings liefert das lala.cgi script nun keine STATISTIC Datenblöcke mehr aus. Daher sind nur noch die Momentanverbräuche nutzbar.
> Damit ist der Scaper quasi unbrauchbar.


Der senec_exporter stellt die Anlagendaten des PV-Wechselrichters im Prometheus Format zur Verfügung.

Thanks to Nancy Chauhan for sharing her HTTP Exporter sample: 
https://levelup.gitconnected.com/building-a-prometheus-exporter-8a4bbc3825f5

Getestet mit **SENEC.Home V3 hybrid duo** mit 3 x 2,5 kWh Akkus. Andere SENEC Wechselrichter sollten ebenfalls funktionieren. Basis für den Exporter ist das lala.cgi Skript auf der Web-Seite des Wechselrichters.

## Funktionsweise
Die Anlagendaten werden per HTTP aus dem Wechselrichter gelesen und über einen eigene HTTP-Server im Prometheus-Format bereitgestellt. Außerdem ist noch eine Aufbereitung im json-Format vorgesehen, um Pull-Basierte Abfragen der Anlagendaten zu ermöglichen. Zum Beispiel mit node-red.

Umgebungsvariablen für den senec_exporter:

|Variable      | Beschreibung                 |
|--------------|------------------------------|
|`SENEC_IP`    | IP des SENEC Wechselrichters |
|`SAMPLE_RATE` | Abtastrate in Sekunden       |

Alternativ können auch Parameter übergeben werden.
```
-ip / --senec-ip = ip address of the senec device e.g. 192.168.1.7 (required) 

-r / --rate = sampling rate in seconds (default=20)

-p / --port = HTTP-Server port where the Prometheus data will be exposed (default=8000)
```
Alternativ können auch Parameter übergeben werden.

Install requirements:
`pip3 install -r requirements.txt`

Start locally with:

`python3 senec_exporter.py -ip 192.168.1.7 -r 5`


## Docker 

Der senec_exporter kann problemlos in einem Docker Container laufen. Der Ressourcenbedarf ist überschaubar. Bei mir läuft der senec_exporter mit vielen anderen Containern zusammen auf einem Raspberry Pi 4 mit 4GB Hauptspeicher.

Create a Docker Image with:

`docker build -t senec_exporter_app -f docker/Dockerfile .`

Start with:

`docker run -p 8000:8000 --restart unless-stopped --name senec_exporter senec_exporter_app`


## Endpunkte
- http://localhost:8000/
- http://localhost:8000/metrics
- http://localhost:8000/json
