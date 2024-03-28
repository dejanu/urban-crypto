# urban-crypto

## Scope
* Set up a K8S cluster with the latest stable version, with RBAC enabled.
* K8S cluster should have 2 services deployed – Service A and Service B.
* Cluster should have NGINX Ingress controller deployed, and corresponding ingress rules for Service A and Service B.
* The following cluster buildout should be secure, repeatable, and automated as much as possible.

* Service A is a WebServer written in C#, Go or Python that exposes the following:
  * Current value of Bitcoin in USD (updated every 10 seconds taken from an API on the web, like https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD).
  * Average value over the last 10 minutes.
* Service B is a REST API service, that exposes a single controller that responds 200 status code on GET requests.
* Service A should not be able to communicate with Service B.

### IaC: Create AKS using Terraform

* Prerequisite azure service principal

```bash
# replace svp credentials
cat<<EOF>>env_vars.sh
export ARM_SUBSCRIPTION_ID="<azure_subscription_id>"
export ARM_TENANT_ID="<azure_subscription_tenant_id>"
export ARM_CLIENT_ID="<service_principal_appid>"
export ARM_CLIENT_SECRET="<service_principal_password>"
EOF

# load svp  and verify credentials  env vars
source env_vars.sh
printenv | grep ^ARM*
```

* Create AKS cluster:
```bash
cd infra/aks
terraform apply
```
* Deploy services:
```bash
# check context (should match the value of terraform "clustername" variable)
kubectl --kubeconfig infra/aks/kubeconfig config current-context

# create resources(deploy/svc/ingress)
kubectl --kubeconfig infra/aks/kubeconfig apply -f apps/k8s_resources
```
### Documentation

* App Documentation [here](https://github.com/dejanu/urban-telegram/blob/main/apps/readme.md)

* Infra Documentation [here](https://github.com/dejanu/urban-telegram/blob/main/infra/readme.md)




