# Issue #150 from pulsar-client-python

See also https://github.com/apache/pulsar-client-python/issues/150

### Try to reproduce the issue

```bash
docker compose up -d pulsar
docker compose run --rm task
docker compose run --rm task
docker compose run --rm task
docker compose up case
```
