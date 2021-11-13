# Prometheus Exporter für SENEC PV Anlage

Thanks to Nancy Chauhan for sharing her HTTP Exporter sample: 
https://levelup.gitconnected.com/building-a-prometheus-exporter-8a4bbc3825f5

start locally with:

`python3 senec_exporter.py`


Create a Docker Image with:

`docker build -t senect_export_app -f docker/Dockerfile .`

Start with:

`docker run -p 8000:8000 --rm --name TEST senect_export_app`

->> http://localhost:8000/