## Terraform

* Authenticating to Azure via Service Principal
```bash
az login

# get subscriptions
az account list -o table --all

# set subscription  
az account set --subscription <subscription_ID>

# list resource groups
az group list -o table

# list service principals
az ad sp list --query "[].{id:id,name:displayName}" --show-mine

# create svp
az ad sp create-for-rbac --name <service_principal_name> --role Contributor --scopes /subscriptions/<subscription_id>

# service principal authentication tokens 
appId is the client_id defined above.
password is the client_secret defined above.
tenant is the tenant_id defined above.
```

* Usage:

```bash
# initialize working directory
terraform init

# linting of TF files
terraform validate


# generates a speculative execution plan
terraform plan

# create execution plan to preview changes and resource dependencies 
terraform plan -out create.tfplan

# analyze tf execution plan: summary of the changes to be made, categorized by “to add,” “to change,” or “to destroy.”

# interactive apply the changes
terraform apply

# apply the changes required to reach the desired state of the configuration
terraform apply main.tfplan

# proposed destroy changes without executing them
terraform plan -destroy -out destroy.tfplan
terraform apply destroy.tfplan

# backend: where Terraform stores its state data files
# by default Terraform uses LOCAL backend, that stores state as local file on disk
# remote backend

```

* State file is either stored **locally** (alternatively a remote backend can be used).

* Check infra:
```bash
# check k8s context
kubectl config current-context

# install unmanaged ingress controller
kubectl apply -f ../ingress_controller/ingress_controller.yaml

# check ingress class name
kubectl  get ingressclasses.networking.k8s.io

# To enable RBAC, start the API server with the --authorization-mode flag set to a comma-separated list that includes RBAC; for example kube-apiserver --authorization-mode=Example,RBAC  ...

# check if RBAC is enabled for AKS
az aks list -o table
az aks show -g <resource group name> -n <cluster name> --query enableRbac

# check DNS zone
az aks show --resource-group <resource group name> --name <cluster name> --query addonProfiles.httpApplicationRouting.config.HTTPApplicationRoutingZoneName

# get creds for AKS (values are set in terraform vars)
az aks get-credentials --resource-group sre-demo --name demoaks -o yaml
```

## Links

* [aks-terraform](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-terraform?tabs=bash&pivots=development-environment-azure-cli)

* [azurerm_kubernetes_cluster](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster)

* Providers: [azurerm](https://github.com/hashicorp/terraform-provider-azurerm)

* [AKS networking](https://learn.microsoft.com/en-us/azure/aks/concepts-network)
