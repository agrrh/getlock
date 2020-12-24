# Info

>Distributed locks for everyone!

[GetLock.tech](https://getlock.tech/) service exists for those who need to get some kind of session lock or simple semaphore-like mechanism.

Actual case was absence of proper concurrency limit for [BitBucket Pipelines](https://jira.atlassian.com/browse/BCLOUD-12821).

# Usage

### `PUT https://getlock.tech/v1/<uuid>`

Create new lock or update existing one.

Params:

- `ttl` - float, in seconds, default is `60.0`.

Response codes:

- `201` created
- `200` refreshed

### `GET https://getlock.tech/v1/<uuid>`

Check if lock is active.

Response codes:

- `423` for active
- `404` for other cases

### `DELETE https://getlock.tech/v1/<uuid>`

Release existing lock.

Response codes:

- `200` success
- `404` lock not found

## Example

Let's say we have some task which takes up to 1 hour yet could be triggered from number of workers. It concurrency required to be limited to single worker at a time.

We choose some random yet valid [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) as our job ID. It should be the same for all workers you decide to limit concurrency for:

```
YOUR_JOB_UUID=28c9c1be-7bb8-4e8c-b22e-c16402a421d5
```

Worker logic then could look like following:

```sh
echo "Checking if another job is running ..."

while [ "$(curl \"https://getlock.tech/v1/${YOUR_JOB_UUID}\" | jq '.locked')" = "true" ]; do
  echo "Locked, waiting for free spot ..."
  sleep 1
done

echo "Free spot found"

echo "Acquiring lock ..."

# NOTE Prefer lower TTL values while refreshing lock periodically
#   to not waste time in case job has failed
curl -X PUT -d ttl=3600 "https://getlock.tech/v1/${YOUR_JOB_UUID}"

echo "Starting payload ..."

sleep 2400

echo "Payload done"

echo "Releasing lock ..."

curl -X DELETE "https://getlock.tech/v1/${YOUR_JOB_UUID}"

echo "Job done"
```

I also recommend you to consider using awesome [httpie](https://httpie.io/) tool.

# Credits

- [Consul Sessions](https://www.consul.io/api-docs/session) - inspiration
- [agrrh](https://agrrh.com/) - implementation
