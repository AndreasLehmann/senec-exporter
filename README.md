# Prometheus Exporter für SENEC PV Anlage

Thanks to Nancy Chauhan for sharing her HTTP Exporter sample: 
https://levelup.gitconnected.com/building-a-prometheus-exporter-8a4bbc3825f5

Allowed arguments:

```
-ip / --senec-ip = ip address of the senec device e.g. 192.168.1.7 (required) 

-r / --rate = sampling rate in seconds (default=20)
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