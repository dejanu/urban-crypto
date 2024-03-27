* Start app:

```bash
# docker container
docker run --rm -p 8888:8888 dejanualex/app_b:1.0

# check endpoints
curl http://127.0.0.1:8888/

# create pod with curl and openssl
kubectl run curlopenssl -i --tty --image=dejanualex/curlopenssl:1.0  -- sh
curl svc-b.default.svc.cluster.local:8888/
```