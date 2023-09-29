# Issue #153 from pulsar-client-python

See also https://github.com/apache/pulsar-client-python/issues/153

### How to reproduce the issue

```bash
docker compose up -d pulsar
docker compose up case
```

In another terminal:

```bash
./health-req.sh  # call x times to see the issue in the `case` container logs
```
