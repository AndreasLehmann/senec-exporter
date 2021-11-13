FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./*.py ./

EXPOSE 8000

CMD [ "python", "senec_exporter.py" ]
