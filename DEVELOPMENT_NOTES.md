# Developer Notes - how to contribute and configure for development


## How to configure Open Telemetry and local Signoz instance

Current project has integration with telemetry - it uses OpenTelemetry library to send traces for the operations run.
In order to configure it for Docker containers execution - please do the following:

1. create a file `.env_docker` - it will be picked up during the docker containers creation
2. Add the following content to the file:
```
# Open Telemetry metrics
OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4318
```




## How to configure direct access to the backend services from web ui without proxy

This could be usefull for big databases - when queries take a long time, and proxy returns timeouts.

1. create a file `.env_docker` - it will be picked up during the docker containers creation
2. Add the following content to the file:
```
# Local configuration - use backend directly, without proxy (for large DB with long operations)
# SERVICE_HOST=192.168.0.81
SERVICE_PORT=9092

FLASK_CORS=True
```

See the description of the values:
* `FLASK_CORS` is required - otherwise it will reject the data coming from the different domain, because web UI is running on 9090, but backed is available on 9092 which is treated a different host.

* `SERVICE_HOST` is not required if the backend services are running on the same host as web - it will pick up the host name form the window.location.hostname .
```js
let service_host = window.SERVICE_HOST ? window.SERVICE_HOST : window.location.hostname;
```