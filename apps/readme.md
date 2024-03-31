## appA

* Virtual Environment:

```bash
# create .venv virtual environment
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

* Start app:

```bash
# local
export FLASK_APP=appa.py
flask run --host=0.0.0.0

# docker container
docker run --rm -p 5000:5000 dejanualex/app_a:1.0

# check endpoints
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/now
curl http://127.0.0.1:5000/avg

# create pod with curl and openssl
kubectl run curlopenssl -i --tty --image=dejanualex/curlopenssl:1.0  -- sh
curl svc-a.default.svc.cluster.local:5000/tensec
```

## appB

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

## K8S resource

* Imperative
```bash
# deployments
kubectl create deploy app-a --image=dejanualex/app_a:1.0 --port=5000
kubectl create deploy app-b --image=dejanualex/app_b:1.0 --port=8888

# services
kubectl -n default  expose deployment app-a --name=svc-a --port=5000 --target-port=5000
kubectl -n default  expose deployment app-b --name=svc-b --port=8888 --target-port=8888

# ingress resource
kubectl create ingress crypto-ingress --class=ngnix --rule="world.universe.mine/svca*=svc-a:5000" --rule="world.universe.mine/svcb*=svc-b:8888"

```
* Declarative
```bash
kubectl apply -f k8s_resources/
```