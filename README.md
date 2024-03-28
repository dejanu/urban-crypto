# urban-crypto

## Scope
* Set up a K8S cluster with the latest stable version, with RBAC enabled.
* The K8S cluster should have 2 services deployed – Service A and Service B.
* Cluster should have NGINX Ingress controller deployed, and corresponding ingress rules for Service A and Service B.
* The following cluster buildout should be secure, repeatable, and automated as much as possible.

* Service A is a WebServer written in C#, Go or Python that exposes the following:
  * Current value of Bitcoin in USD (updated every 10 seconds taken from an API on the web, like https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD).
  * Average value over the last 10 minutes.
* Service B is a REST API service, that exposes a single controller that responds 200 status codes on GET requests.
* Service A should not be able to communicate with Service B.

### Steps

* IaC: Create AKS using Terraform:

```bash
# Prerequisite azure service principa
# replace svp credentials
cat<<EOF>env_vars.sh
export ARM_SUBSCRIPTION_ID="<azure_subscription_id>"
export ARM_TENANT_ID="<azure_subscription_tenant_id>"
export ARM_CLIENT_ID="<service_principal_appid>"
export ARM_CLIENT_SECRET="<service_principal_password>"
EOF
```

```bash
# load svp credentials as env vars
source env_vars.sh
printenv | grep ^ARM*
```

* Create AKS cluster:
```bash
cd infra/aks
terraform init
terraform apply
```
* Create DNS record in Azure portal:
```bash
# get DNS zone 
az aks show -g sre_resourcegroup -n sreaks --query addonProfiles.httpApplicationRouting.config.HTTPApplicationRoutingZoneName

# add addon-http-application-routing-nginx-ingress kube-system public IP as A record in the created DNS zone

# update in-place the ingress resource with desired A record
yq -i e '.spec.rules[].host |= "INSERT_RECORD"' apps/k8s_resources/ingress.yaml
```
* Deploy services:
```bash
# check context (should match the value of terraform "clustername" variable)
kubectl --kubeconfig infra/aks/kubeconfig config current-context

# install nginx ingress controller
kubectl --kubeconfig infra/aks/kubeconfig apply -f infra/ingress_controller/

# create resources(deploy/svc/ingress)
kubectl --kubeconfig infra/aks/kubeconfig apply -f apps/k8s_resources/

# test services
kubectl --kubeconfig infra/aks/kubeconfig run -it curlopenssl  --image=dejanualex/curlopenssl:1.0  -- sh
curl svc-b.default.svc.cluster.local:8888/
curl svc-a.default.svc.cluster.local:5000/
```

### Cleanup

```bash
kubectl --kubeconfig infra/aks/kubeconfig delete -f infra/ingress_controller/
kubectl --kubeconfig infra/aks/kubeconfig delete -f apps/k8s_resources/
cd infra/aks && terraform destroy
```
### Documentation

* App Documentation [here](https://github.com/dejanu/urban-crypto/blob/main/apps/readme.md)

* Infra Documentation [here](https://github.com/dejanu/urban-crypto/blob/main/infra/readme.md)
