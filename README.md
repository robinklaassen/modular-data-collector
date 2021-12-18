# modular-data-collector
Ingest data from API's and store them wherever!


## Developing

### InfluxDB

Testing the connection to InfluxDB on your local machine is easiest using Docker:

```commandline
docker run -d --name=influxdb -p 8086:8086 influxdb:2.1
```

You can also mount a local volume using `-v` if you like. When running the first time,
you should go to http://localhost:8086 to setup an initial user and bucket.