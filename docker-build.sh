
docker build -t senec_exporter_app -f docker/Dockerfile .
docker tag senec_exporter_app nas01.local:5500/senec_exporter


